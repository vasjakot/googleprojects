import gdata.analytics.client
import gdata.sample_util

def main():

    demo = DataFeedDemo()
    demo.PrintFeedDetails()
    demo.PrintDataSources()
    demo.PrintFeedAggregates()
    demo.PrintSegmentInfo()
    demo.PrintOneEntry()
    demo.PrintFeedTable()


class DataFeedDemo(object):

    def __init__(self):
        SOURCE_APP_NAME = 'Google-dataFeedDemoPython-v2'
        my_client = gdata.analytics.client.AnalyticsClient(source=SOURCE_APP_NAME)

        try:
            gdata.sample_util.authorize_client(
                my_client,
                service=my_client.auth_service,
                source=SOURCE_APP_NAME,
                scopes=['https://www.google.com/analytics/feeds/'])
        except gdata.client.BadAuthentication:
            exit('Invalid user credentials given.')
        except gdata.client.Error:
            exit('Login Error')

        # DataFeedQuery simplifies constructing API queries and uri encodes params.
        data_query = gdata.analytics.client.DataFeedQuery({
            'ids': "ga:56169832",
            'start-date': '2012-03-01',
            'end-date': '2012-03-03',
            'dimensions': 'ga:source,ga:medium',
            'metrics': 'ga:visits',
            'sort': '-ga:visits',
            'filters': 'ga:medium==referral',
            'max-results': '50'})

        self.feed = my_client.GetDataFeed(data_query)

    def PrintFeedDetails(self):
        """Prints important Analytics related data found at the top of the feed."""

        print '\n-------- Feed Data --------'
        print 'Feed Title          = ' + self.feed.title.text
        print 'Feed Id             = ' + self.feed.id.text
        print 'Total Results Found = ' + self.feed.total_results.text
        print 'Start Index         = ' + self.feed.start_index.text
        print 'Results Returned    = ' + self.feed.items_per_page.text
        print 'Start Date          = ' + self.feed.start_date.text
        print 'End Date            = ' + self.feed.end_date.text
        print 'Has Sampled Data    = ' + str(self.feed.HasSampledData())

    def PrintDataSources(self):
        """Prints data found in the data source elements.

        This data has information about the Google Analytics account the referenced
        table ID belongs to. Note there is currently exactly one data source in
        the data feed.
        """

        data_source = self.feed.data_source[0]

        print '\n-------- Data Source Data --------'
        print 'Table ID        = ' + data_source.table_id.text
        print 'Table Name      = ' + data_source.table_name.text
        print 'Web Property Id = ' + data_source.GetProperty('ga:webPropertyId').value
        print 'Profile Id      = ' + data_source.GetProperty('ga:profileId').value
        print 'Account Name    = ' + data_source.GetProperty('ga:accountName').value

    def PrintFeedAggregates(self):
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

    def PrintSegmentInfo(self):
        """Prints segment information if the query has advanced segments
        defined."""

        print '-------- Advanced Segments Information --------'
        if self.feed.segment:
            if segment.name:
                print 'Segment Name       = ' + str(segment.name)
            if segment.id:
                print 'Segment Id         = ' + str(segment.id)
            print 'Segment Definition = ' + segment.definition.text
        else:
            print 'No segments defined'

    def PrintOneEntry(self):
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

    def PrintFeedTable(self):
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


if __name__ == '__main__':
    main()