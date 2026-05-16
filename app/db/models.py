from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, JSON, Enum as SQLAlchemyEnum, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class MemberRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    telegram: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    profiles: Mapped[List["Profile"]] = relationship(
        "Profile", back_populates="user", cascade="all, delete-orphan"
    )
    refresh_token: Mapped[str] = mapped_column(nullable=False)



class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True, default=list)

    user: Mapped["User"] = relationship("User", back_populates="profiles")
    meeting_memberships: Mapped[List["MeetingMember"]] = relationship(
        "MeetingMember", back_populates="profile", cascade="all, delete-orphan"
    )
    created_meetings: Mapped[List["Meeting"]] = relationship(
        "Meeting", back_populates="creator"
    )


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    starts_at: Mapped[datetime] = mapped_column(nullable=False)
    ends_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_by: Mapped[Optional[int]] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"),nullable=True)

    # Убрал foreign_keys - SQLAlchemy сам подставит created_by
    creator: Mapped[Optional["Profile"]] = relationship(
        "Profile", back_populates="created_meetings"
    )
    members: Mapped[List["MeetingMember"]] = relationship(
        "MeetingMember", back_populates="meeting", cascade="all, delete-orphan"
    )


class MeetingMember(Base):
    __tablename__ = "meeting_members"
    __table_args__ = (
        UniqueConstraint('meeting_id', 'profile_id', name='uq_meeting_profile'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[MemberRole] = mapped_column(
        SQLAlchemyEnum(MemberRole), nullable=False, default=MemberRole.MEMBER
    )

    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="members")
    profile: Mapped["Profile"] = relationship("Profile", back_populates="meeting_memberships")