function runViz() 
{
   mapChart('ACCESS');
   lineChart(['Afghanistan','United Arab Emirates','Argentina'], 'Afghanistan, United Arab Emirates, Argentina', 'ACCESS');

   $("#map_submit_button").click(function() {
         var indicator_selection_id = $('#map_indicator_list').select2("val");
         var indicator_selection_name = $('#map_indicator_list').select2("data");

         mapChart(indicator_selection_id[0]);
   });

   $("#line_submit_button").click(function() {
      // mapChart();
      var countryselection_id = $('#country_list').select2("val");
      var countryselection_name = $('#country_list').select2("data");  

      var indicator_selection_id = $('#line_indicator_list').select2("val");
      var indicator_selection_name = $('#line_indicator_list').select2("data");

      var countries = []
      var names_countries = '';

      for (var i = 0; i < countryselection_id.length; i++) 
      {
         countries[i] = countryselection_id[i]
         names_countries = names_countries.concat(countries[i].concat(', '));
      };

      // remove trailing ', '
      names_countries = names_countries.slice(0, -2);
      lineChart(countries, names_countries, indicator_selection_id[0]);
   });



   function runCharts(countryselection_id, indicator_selection_id, indicator_selection_name) 
   {
      // User Input of Country Names
         // var countries = prompt("Please enter a list of countries separated by commas with First Letter Capital:", "India, China, Afghanistan");
         // var countries = countries.split(',');
         // var names_countries = '';

      var countries = []
      var names_countries = '';

      for (var i = 0; i < countryselection_id.length; i++) 
      {
         countries[i] = countryselection_id[i]
         // countries[i] = countries[i].replace(/\s+/g, '');
         names_countries = names_countries.concat(countries[i].concat(', '));
         // alert(AllData[countries[i]]["iso"]);
      };

      // remove trailing ', '
      names_countries = names_countries.slice(0, -2);

      // User Input of Indicator
         // var indicator = prompt("Please enter the name of one indicator\n Here are some options:", "EPI, NO2, PM25");
         // var indicator = indicator.split(',');
         // indicator = indicator[0].replace(/\s+/g, '');
         // indicator = indicator.toUpperCase();

      var indicator = indicator_selection_id[0];
      // alert(indicator);
      // alert(typeof indicator[0]);
      // alert(map_lookup);
      // alert(ACCESS_MAP);

      mapChart(indicator);
      lineChart(countries, names_countries, indicator);
   };

   function mapChart(indicator) 
   {
     // Add lower case codes to the data set for inclusion in the tooltip.pointFormat
      var title = {
             text: 'Fixed tooltip with HTML'
      };

      var legend = {
             title: {
                 text: 'Population density per km²',
                 style: {
                     color: (Highcharts.theme && Highcharts.theme.textColor) || 'blue'
                 }
             }
      };

      var mapNavigation = {
             enabled: true,
             buttonOptions: {
                 verticalAlign: 'bottom'
             }
      };

      var tooltip = {
             backgroundColor: 'none',
             borderWidth: 0,
             shadow: false,
             useHTML: true,
             padding: 0,
             pointFormat: '<span class="f32"><span class="flag {point.flag}"></span></span>' +
                 ' {point.name}: <b>{point.value}</b>/km²',
             positioner: function () {
                 return { x: 0, y: 250 };
             }
      };

      var colorAxis = {
             min: 0,
             max: 100
      };

      var series = [{
             // data : EPI_MAP,
             data : map_lookup[indicator],
             mapData: Highcharts.maps['custom/world'],
             joinBy: ['iso-a2', 'code'],
             name: 'Population density',
             states: {
                 hover: {
                     color: '#BADA55'
                 }
             }
      }];


      var json = {};   
      json.title = title;    
      json.legend = legend;    
      json.mapNavigation = mapNavigation;
      json.tooltip = tooltip;
      json.colorAxis = colorAxis;
      json.series = series;

      $('#MapContainer').highcharts('Map', json); 

   };

   function lineChart(countries, names_countries, indicator) 
   {
      // alert(countries);

      // used as a counter for the number of countries with missing values
      var j = 0;

      var missing_data_countries = []
      // missing_data_countries is an array of all countries that have missing values
      for (var i = 0; i < countries.length; i++) 
      {
         // alert(line_lookup[indicator][countries[i]]["averages"]);

         if (line_lookup[indicator][countries[i]]["averages"] == '' 
               || line_lookup[indicator][countries[i]]["ranges"] == '') 
         {
            missing_data_countries[j] = countries[i].concat(', ');
            j += 1;
         }
      }

      if (j > 0)
      {
         // remove trailing ', '
         missing_data_countries[j-1] = missing_data_countries[j-1].slice(0, -2);
      }
      

      var title = {
         text: 'Plot of '.concat(indicator).concat(' Indicator for ').concat(names_countries)
      };    
      var xAxis = {
         type: 'year'     
      };
      var yAxis = {
         min: 0,
         max: 100,
         title: {
            text: indicator
         }      
      };
      var tooltip = {
          shared: true,
         crosshairs: true,
          valueSuffix: '%'
      };
      var legend = {      
      };    
      var noData = {
               style: {
                   fontWeight: 'bold',
                   fontSize: '15px',
                   color: 'red'
               },
               position: {
                  "x": 5, 
                  "y": 0, 
                  "align": "left", 
                  "verticalAlign": "bottom" 
               },
      };

      var series = [];

      for (var i = 0; i < countries.length; i++) 
      {
         series[2*i] = {
            name: countries[i] + ' Median',
               data: line_lookup[indicator][countries[i]]["averages"],
               zIndex: 1,
               marker: {
                   fillColor: 'white',
                   lineWidth: 2,
                   lineColor: Highcharts.getOptions().colors[i]
               }
           }; 

         series[2*i+1] = {
               name: countries[i] + ' Range',
               data: line_lookup[indicator][countries[i]]["ranges"],
               type: 'arearange',
               lineWidth: 0,
               linkedTo: ':previous',
               color: Highcharts.getOptions().colors[i],
               fillOpacity: 0.3,
               zIndex: 0
         };
         // alert(countries[i]);
      };

      var json = {};   
      json.title = title;    
      json.xAxis = xAxis;
      json.yAxis = yAxis;
      json.tooltip = tooltip;
      json.legend = legend;     
      json.series = series;


      if (missing_data_countries.length > 0) 
      {
         json.noData = noData;
      }


      $('#LineContainer').highcharts(json); 
      chart = $('#LineContainer').highcharts();

      if (missing_data_countries.length > 0) 
      {
         chart.showNoData(indicator.concat(" data for ".concat(missing_data_countries).concat(" is missing")));
      }
   }
};