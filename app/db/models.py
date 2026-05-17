from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, JSON, Enum as SQLAlchemyEnum, UniqueConstraint, ForeignKey, DateTime
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
    refresh_token: Mapped[str] = mapped_column(nullable=False)

    friends: Mapped[List["Friend"]] = relationship(
        "Friend",
        back_populates="user",
        foreign_keys="[Friend.user_id]",
        cascade="all, delete-orphan"
    )
    profiles: Mapped[List["Profile"]] = relationship(
        "Profile", back_populates="user", cascade="all, delete-orphan"
    )



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



class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ends_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    creator: Mapped[Optional["Profile"]] = relationship(
        "Profile", back_populates="created_meetings"
    )
    members: Mapped[List["MeetingMember"]] = relationship(
        "MeetingMember", back_populates="meeting", cascade="all, delete-orphan"
    )


class MeetingMember(Base):
    __tablename__ = "meeting_members"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[MemberRole] = mapped_column(
        SQLAlchemyEnum(MemberRole), nullable=False, default=MemberRole.MEMBER
    )

    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="members")
    profile: Mapped["Profile"] = relationship("Profile", back_populates="meeting_memberships")

    __table_args__ = (
        UniqueConstraint('meeting_id', 'profile_id', name='uq_meeting_profile'),
    )

class Friend(Base):
    __tablename__ = 'friends'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    accept: Mapped[bool] = mapped_column(nullable=True)

    user = relationship('User', foreign_keys=[user_id], back_populates='friends')
    friend = relationship('User', foreign_keys=[friend_id])

