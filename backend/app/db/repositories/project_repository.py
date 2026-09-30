from typing import Optional

from sqlalchemy.orm import Session

from app.models.project import ProjectConceptNote


def create_project(
    db: Session,
    payload: dict,
):
    project = ProjectConceptNote(**payload)

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_project(
    db: Session,
    project_id: int,
):
    return (
        db.query(ProjectConceptNote)
        .filter(
            ProjectConceptNote.id == project_id
        )
        .first()
    )


def get_projects(
    db: Session,
    *,
    hotspot_id: Optional[int] = None,
    limit: int = 500,
):
    query = db.query(ProjectConceptNote)

    if hotspot_id:
        query = query.filter(
            ProjectConceptNote.hotspot_id
            == hotspot_id
        )

    return (
        query
        .order_by(ProjectConceptNote.id.desc())
        .limit(limit)
        .all()
    )