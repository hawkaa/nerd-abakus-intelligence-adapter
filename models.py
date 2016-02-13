from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Table, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import object_session
import re

import settings
import datetime

Base = declarative_base()

survey_submission_table = Table(
    'survey_surveysubmission',
    Base.metadata,
    Column('survey_id', ForeignKey('survey_survey.id'), primary_key = True),
    Column('user_id', ForeignKey('core_user.id'), primary_key = True)
)

class User(Base):
    __tablename__ = 'core_user'

    id = Column('id', Integer, primary_key = True)
    username = Column('username', String)
    first_name = Column('name', String)
    last_name = Column('surname', String)
    deleted = Column('deleted', Boolean)
    mail = Column('mail', String)

    _isProgramClassRead = False
    _program = None
    _class = None

    # Relationships
    memberships = relationship('Membership', back_populates = 'user')
    surveys = relationship('Survey', secondary = survey_submission_table, back_populates = 'users')

    def __repr__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def getClass(self):
        self._setProgramAndClass()
        return self._class

    def getProgram(self):
        self._setProgramAndClass()
        return self._program

    def getGender(self):
        questions = self._getGenderQuestions()
        for question in questions:
            answer = question.getAnswerForUser(self)
            if re.search(settings.MALE_REGEX, str(answer), re.IGNORECASE): return 'Mann'
            elif re.search(settings.FEMALE_REGEX, str(answer), re.IGNORECASE): return 'Kvinne'
        return 'Ukjent'

    def _setProgramAndClass(self):
        if self._isProgramClassRead: return
        self._isProgramClassRead = True
        membership = object_session(self).query(Membership)\
            .join(Group)\
            .join(Role)\
            .filter(Membership.user_id == self.id)\
            .filter(Group.name.in_(settings.PROGRAM_GROUP_NAMES))\
            .filter(Role.name.in_(settings.CLASS_ROLE_NAMES))\
            .filter(Membership.from_date > datetime.datetime.now() - datetime.timedelta(days = settings.MEMBERSHIP_VALID))\
            .first()
        if membership:
            self._program = membership.group.name
            self._class = membership.role.name[0]

    def _getGenderQuestions(self):
        questions = []
        for survey in self.surveys:
            for question in survey.questions:
                if re.search('KJØNN', question.question, re.IGNORECASE):
                    questions.append(question)
        return questions





class Role(Base):
    __tablename__ = 'core_role'

    id = Column(Integer, primary_key = True)
    deleted = Column(Boolean)
    name = Column(String)

    def __repr__(self):
        return self.name

class Group(Base):
    __tablename__ = 'core_group'

    id = Column(Integer, primary_key = True)
    deleted = Column(Boolean)
    name = Column(String)

    def __repr__(self):
        return self.name

class Membership(Base):
    __tablename__ = 'core_membership'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('core_user.id'))
    group_id = Column(Integer, ForeignKey('core_group.id'))
    role_id = Column(Integer, ForeignKey('core_role.id'))
    from_date = Column(DateTime)

    user = relationship('User', back_populates = 'memberships')
    group = relationship('Group')
    role = relationship('Role')

    def __repr__(self):
        return '<%s, %s, %s>' % (self.user, self.group, self.role)

class Survey(Base):
    __tablename__ = 'survey_survey'
    id = Column(Integer, primary_key = True)
    title = Column(String)
    created = Column(Date)

    questions = relationship('SurveyQuestion', back_populates = 'survey')
    users = relationship('User', secondary = survey_submission_table, back_populates = 'surveys')

    def __repr__(self):
        return '<%s, %s>' % (self.title, self.created)

class SurveyQuestion(Base):
    __tablename__ = 'survey_question'
    id = Column(Integer, primary_key = True)
    survey_id = Column(Integer, ForeignKey('survey_survey.id'))
    question = Column(String)

    survey = relationship('Survey', back_populates = 'questions')
    alternatives = relationship('SurveyAlternative', back_populates = 'question')

    def getAnswerForUser(self, user):
        answer = object_session(self).query(SurveyAlternative)\
            .join(SurveyQuestion)\
            .join(SurveyResult)\
            .filter(SurveyResult.user_id == user.id)\
            .filter(SurveyAlternative.question_id == self.id).first()
        if answer:
            return str(answer)
        return None


    def __repr__(self):
        return self.question

class SurveyAlternative(Base):
    __tablename__ = 'survey_alternative'
    id = Column(Integer, primary_key = True)
    alternative = Column(String)
    question_id = Column(Integer, ForeignKey('survey_question.id'))

    question = relationship('SurveyQuestion', back_populates = 'alternatives')
    results = relationship('SurveyResult', back_populates = 'alternative')

    def __repr__(self):
        return self.alternative

class SurveyResult(Base):
    __tablename__ = 'survey_surveyresult'
    id = Column(Integer, primary_key = True)
    alternative_id = Column(Integer, ForeignKey('survey_alternative.id'))
    user_id = Column(Integer, ForeignKey('core_user.id'))
    survey_id = Column(Integer, ForeignKey('core_user.id'))

    alternative = relationship('SurveyAlternative', back_populates = 'results')

class Event(Base):
    __tablename__ = 'event_event'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    type_id = Column(Integer, ForeignKey('event_eventtype.id'))
    intro = Column(Text)
    location = Column(String)
    capacity = Column(Integer)
    is_registration_required = Column(Boolean)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    feedback_when_registering = Column('feedback_when_registrating', Boolean)
    price_members = Column(Integer)
    price_guests = Column(Integer)

    type = relationship('EventType')


class EventType(Base):
    __tablename__ = 'event_eventtype'
    id = Column(Integer, primary_key = True)
    name = Column(String)
