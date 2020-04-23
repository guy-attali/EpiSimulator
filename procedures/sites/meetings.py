from procedures.base import SiteProcedure
from core.world import world
from sites.base import Site

from traits.base import PERSON_TRAIT_TYPE


class Meeting:
    """
    Represents a single Meeting between two or more people
    """
    def __init__(self, person1, person2, site):
        self._time = world.current_ts
        self._people_involved = [person1, person2]
        self._location = site

    def __repr__(self):
        string = "Meeting(Location: {0} \n \t person1: {1} \n \t person2: {2} \n \t meeting time: {3} \n \t is meeting infected: {4}".format(
            self._location, str(self._people_involved[0].uuid), str(self._people_involved[1].uuid),
            self._time, self.is_meeting_infected()
        )
        return string

    def __str__(self):
        string = "Meeting(Location: {0} \n person1: {1} \n person2: {2} \n meeting time: {3} \n is meeting infected: {4}".format(
            self._location, str(self._people_involved[0].uuid), str(self._people_involved[1].uuid), self._time,
            self.is_meeting_infected()
        )
        return string

    def update_log(self):
        """
        writes down the meeting object in a log.txt file
        work in progress.
        """
        pass

    def is_meeting_infected(self):
        """
        checks if one of the people in the meeting is infected.
        :return boolean
        """
        return self._people_involved[1].traits[PERSON_TRAIT_TYPE.INFECTED] or\
               self._people_involved[0].traits[PERSON_TRAIT_TYPE.INFECTED]


class MeetingProcedureSite(SiteProcedure):
    def apply(self, site: Site):
      """
      checks for meetings randomly using the meeting probability.
      if the randomized number is in the range of the meeting probability a 'Meeting' object is created.
      :return list of meetings that occured in the 'Site'.
              if no meetings were created returns an empty list.
      """
      meetings = []
      meeting_probability = self.calculate_meeting_probability(site, time_step=world.time_step)
      if meeting_probability > 0:
          for id, person1 in site.people:
              if random.uniform(0, 1) <= meeting_probability:
                  person2 = random.choice([person for person in self.get_peoples() if person != person1])
                  meeting = Meeting(person1=person1, person2=person2, site=self)
                  meetings.append(meeting)

      return meetings

    def calculate_meeting_probability(self, site, time_step):
        """
        calculates the meeting probabilty in a 'Site' in a certain moment.
        multiplying the number of people in square meters with the dispersion factor.
        the meeting probability is in scale of 0 to 1.
        :param time_step - the time intervals
        """
        if len(site.people) < 2:
            return 0
        else:
            m_p = (len(site.people)*time_step/site.area)*site.dispersion_factor
            return m_p if m_p < 1 else 1

    def should_apply(self, site: Site) -> bool:
        return True
