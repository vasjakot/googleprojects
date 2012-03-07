#!/usr/bin/python

import gdata.analytics.client
import gdata.sample_util

#email = 'craig.tenthwave@gmail.com'.encode("utf-8")
#password = '3spr3ss0'.encode("utf-8")
#email='eugineosipov@gmail.com'
#password='preferans'



def main():
    """
    Main function
    """
    email = "eugineosipov@gmail.com"
    password = "preferans"
    feeds = DataFeed(email,password,0)
    feeds.OneEntry()
    #feeds.FeedDetails()
    #feeds.AdvancedSegments()
    #feeds.CustomVarForOneEntry()
    #feeds.GoalsForOneEntry()
    #feeds.AccountEntries()
    #feeds.FeedAggregates()

class DataFeed(object):
    #connect to google
    def __init__(self, email, password, iterEntry):
        cll      = gdata.analytics.client.AnalyticsClient()
        try:
            cll.ClientLogin(email, password, 'HOSTED_OR_GOOGLE', 'analytics')
        except gdata.client.CaptchaChallenge as challenge:
            print 'Please visit ' + challenge.captcha_url
            answer = raw_input('Answer to the challenge? ')
            cll.ClientLogin(email, password, application_name, captcha_token=challenge.captcha_token,
            captcha_response=answer)
        except gdata.client.BadAuthentication:
            exit('Users credentials were unrecognized')
        except gdata.client.RequestError:
            exit('Login Error')


        account_query = gdata.analytics.client.AccountFeedQuery()
        self.feed = cll.GetAccountFeed(account_query)
        #tab_id = self.AccountEntrie()
        #tab_id = "ga:56169832"
        #data_query = gdata.analytics.client.DataFeedQuery({
            #'ids': tab_id,
            #'start-date': '2012-03-01',
            #'end-date': '2012-03-07',
            #'dimensions': 'ga:source',
            #'metrics': 'ga:visits',
            #'sort': '-ga:visits',
            #'filters': 'ga:medium==referral',
            #'max-results': '50'})
        #self.feed = cll.GetAccountFeed(data_query)

    def OneEntry(self):
        """Prints all the important Google Analytics data found in an entry"""

        print '\n-------- One Entry --------'
        if len(self.feed.entry) == 0:
            print 'No entries found'
            return

        entry = self.feed.entry[0]
        print 'ID      = ' + entry.id.text

        for dim in entry.dimension:
            print 'Dimension Name  = ' + dim.name
            print 'Dimension Value = ' + dim.value

        for met in entry.metric:
            print 'Metric Name     = ' + met.name
            print 'Metric Value    = ' + met.value
            print 'Metric Type     = ' + met.type
            print 'Metric CI       = ' + met.confidence_interval

    def FeedTable(self):
        """Prints all the entries as a table."""

        print '\n-------- All Entries In a Table --------'
        for entry in self.feed.entry:
            for dim in entry.dimension:
                print ('Dimension Name = %s \t Dimension Value = %s'
                       % (dim.name, dim.value))
            for met in entry.metric:
                print ('Metric Name    = %s \t Metric Value    = %s'
                       % (met.name, met.value))
            print '---'

    def FeedDetails(self):
        print '-------- Important Feed Data --------'
        print 'Feed Title          = ' + self.feed.title.text
        print 'Feed Id             = ' + self.feed.id.text
        print 'Total Results Found = ' + self.feed.total_results.text
        print 'Start Index         = ' + self.feed.start_index.text
        print 'Results Returned    = ' + self.feed.items_per_page.text

    def AdvancedSegments(self):
        print '-------- Advances Segments --------'
        if not self.feed.segment:
            print 'No advanced segments found'
        else:
            for segment in self.feed.segment:
                print 'Segment Name       = ' + segment.name
                print 'Segment Id         = ' + segment.id
                print 'Segment Definition = ' + segment.definition.text

    def CustomVarForOneEntry(self):
        print '-------- Custom Variables --------'
        if not self.feed.entry:
            print 'No entries found'
        else:
            for entry in self.feed.entry:
                if entry.custom_variable:
                    for custom_variable in entry.custom_variable:
                        print 'Custom Variable Index = ' + custom_variable.index
                        print 'Custom Variable Name  = ' + custom_variable.name
                        print 'Custom Variable Scope = ' + custom_variable.scope
                    return
            print 'No custom variables defined for this user'

    def GoalsForOneEntry(self):
        print '-------- Goal Configuration --------'
        if not self.feed.entry:
            print 'No entries found'
        else:
            for entry in self.feed.entry:
                if entry.goal:
                    for goal in entry.goal:
                        print 'Goal Number = ' + goal.number
                        print 'Goal Name   = ' + goal.name
                        print 'Goal Value  = ' + goal.value
                        print 'Goal Active = ' + goal.active

                        if goal.destination:
                            self.DestinationGoal(goal.destination)
                        elif goal.engagement:
                            self.EngagementGoal(goal.engagement)
                    return

    def DestinationGoal(self, destination):
        print '----- Destination Goal -----'
        print 'Expression      = ' + destination.expression
        print 'Match Type      = ' + destination.match_type
        print 'Step 1 Required = ' + destination.step1_required
        print 'Case Sensitive  = ' + destination.case_sensitive

        if destination.step:
            print '----- Destination Goal Steps -----'
            for step in destination.step:
                print 'Step Number = ' + step.number
                print 'Step Name   = ' + step.name
                print 'Step Path   = ' + step.path

    def EngagementGoal(self, engagement):
        print '----- Engagement Goal -----'
        print 'Goal Type       = ' + engagement.type
        print 'Goal Engagement = ' + engagement.comparison
        print 'Goal Threshold  = ' + engagement.threshold_value

    def AccountEntries(self):
        print '-------- First 1000 Profiles in Account Feed --------'
        if not self.feed.entry:
            print 'No entries found'
        else:
            for entry in self.feed.entry:
                print 'Web Property ID = ' + entry.GetProperty('ga:webPropertyId').value
                print 'Account Name    = ' + entry.GetProperty('ga:accountName').value
                print 'Account Id      = ' + entry.GetProperty('ga:accountId').value
                print 'Profile Name    = ' + entry.title.text
                print 'Profile ID      = ' + entry.GetProperty('ga:profileId').value
                print 'Table ID        = ' + entry.table_id.text
                print 'Currency        = ' + entry.GetProperty('ga:currency').value
                print 'TimeZone        = ' + entry.GetProperty('ga:timezone').value
                if entry.custom_variable:
                    print 'This profile has custom variables'
                if entry.goal:
                    print 'This profile has goals'

    def AccountEntrie(self):
        table_id = []
        if self.feed.entry:
            for entry in self.feed.entry:
                table_id.append(entry.table_id.text)
        return table_id





    def FeedAggregates(self):
        """Prints data found in the aggregates elements.

        This contains the sum of all the metrics defined in the query across.
        This sum spans all the rows matched in the feed.total_results property
        and not just the rows returned by the response.
        """

        aggregates = self.feed.aggregates

        print '\n-------- Metric Aggregates --------'
        for met in aggregates.metric:
            print ''
            print 'Metric Name  = ' + met.name
            print 'Metric Value = ' + met.value
            print 'Metric Type  = ' + met.type
            print 'Metric CI    = ' + met.confidence_interval

if __name__ == '__main__':
    main()