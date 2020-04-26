import random
from procedures.base import SiteProcedure
from core.world import world
from core.site import Site

<<<<<<< HEAD
=======

>>>>>>> master
class Meeting:
    """
    Represents a single Meeting between two or more people
    """
    def __init__(self, person1, person2, site, timestamp):
        self._time = timestamp
        self._people_involved = [person1, person2]
        self._location = site

    def __repr__(self):
        string = "Meeting(Location: {0} \n \t person1: {1} \n \t person2: {2} \n \t meeting time: {3} \n \t is meeting is_infected: {4}".format(
            self._location, str(self._people_involved[0].uuid), str(self._people_involved[1].uuid),
            self._time, self.is_meeting_infected()
        )
        return string

    def __str__(self):
        string = "Meeting(Location: {0} \n person1: {1} \n person2: {2} \n meeting time: {3} \n is meeting is_infected: {4}".format(
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
        checks if one of the people in the meeting is is_infected.
        :return boolean
        """
<<<<<<< HEAD
        return self._people_involved[1].is_infected or\
               self._people_involved[0].is_infected

=======
        return self._people_involved[1].traits.infected or\
               self._people_involved[0].traits.infected
>>>>>>> master

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
          for person1 in site.people:
              if random.random() <= meeting_probability:
                  person2 = random.choice(list(site.people.difference({person1})))
                  meeting = Meeting(
                      person1=person1,
                      person2=person2,
                      site=site,
                      timestamp=world.current_tf.sample_random_timestamp()
                  )
                  meetings.append(meeting)

      return meetings

    def calculate_meeting_probability(self, site, time_step:timedelta):
        """
        calculates the meeting probabilty in a 'Site' in a certain moment.
        multiplying the number of people in square meters with the dispersion factor.
        the meeting probability is in scale of 0 to 1.
        :param time_step - the time intervals
        """
        if len(site.people) < 2:
            return 0.0
        else:
<<<<<<< HEAD
            m_p = (len(site.people)*(time_step.total_seconds()/60)/site.area)*site.dispersion_factor
            return m_p if m_p < 1.0 else 1.0
=======
            m_p = (len(site.people)*time_step/site.traits.area)*site.traits.dispersion_factor
            return m_p if m_p < 1 else 1
>>>>>>> master

    def should_apply(self, site: Site) -> bool:
        return True
