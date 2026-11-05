from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session


from app.core.deps import require_recruiter
from app.db.session import get_db
from app.models.jobs import Job
from app.models.user import User
from app.schemas.jobs import JobCreate, JobRead, JobUpdate

router = APIRouter(prefix="/jobs", tags=["jobs"])


def get_job_or_404(job_id: int, db: Session) -> Job:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


def ensure_owner(job: Job, user: User) -> None:
    if job.company.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only modify your own company's jobs",
        )


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter),
):
    if current_user.company is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Create your company first",
        )
    job = Job(**payload.model_dump(), company_id=current_user.company.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job




@router.get("", response_model=list[JobRead])
def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Job)
        .where(Job.is_active.is_(True))
        .order_by(Job.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()



@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return get_job_or_404(job_id, db)


@router.patch("/{job_id}", response_model=JobRead)
def update_job(
    job_id: int,
    payload: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter),
):
    job = get_job_or_404(job_id, db)
    ensure_owner(job, current_user)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job




@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter),
):
    job = get_job_or_404(job_id, db)
    ensure_owner(job, current_user)
    db.delete(job)
    db.commit()