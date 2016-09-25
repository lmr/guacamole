/*
 * Guacamole Web Javascript library.
 * Author: Lucas Meneghel Rodrigues <lookkas@gmail.com>
 */

var guacamoleApp = {
    server: guacamoleServer,
    init: function() {
        $( document ).ajaxError(function( event, jqxhr, settings, thrownError ) {
            $( "#errors" ).show();
            if ( settings.url.match( "version/$" )) {
                $( "#errors" ).append( "<p>Could not get server version from " + guacamoleServerSettings.url + "</p>" );
            } else if ( settings.url.match( "jobs/summary/$" ) ) {
                $( "#errors" ).append( "<p>Failed to retrieve jobs summary from " + settings.url +  "</p>" );
            } else if ( settings.url.match( "jobs/" ) ) {
                $( "#errors" ).append( "<p>Failed to retrieve job results from " + settings.url + "</p>" );
            } else if ( settings.url.match( "tests/summary/$" ) ) {
                $( "#errors" ).append( "<p>Failed to retrieve tests summary from " + settings.url + "</p>" );
            } else {
                $( "#errors" ).append( "<p>Generic error on request " + settings.url + "</p>" );
            }
            if (jqxhr.responseText) {
                detail = jQuery.parseJSON( jqxhr.responseText ).detail;
                $( "#errors" ).append( "<p>Reason: " + detail + "</p>" );
            }
        });
        this.server.init(guacamoleServerSettings);
    },
    version: function() {
        this.server.getVersion(function( json ) {
           $( "#info" ).text( "Server version: " + json.version );
        });
    },
    sendFormData: function(formdata, resource, label) {
        var url = guacamoleServerSettings.url + resource;

        var xmlhttp = null;
        if (window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
        }
        else if (window.ActiveXObject) {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }

        xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 201) {
           var response = JSON.parse(xmlhttp.responseText);
           alert( label + " " + response.id + " created" );
           }
        };
        xmlhttp.onloadend = function() {
        if (xmlhttp.status == 404) {
           var response = JSON.parse(xmlhttp.responseText);
           alert(response.message);
           }
        };
        xmlhttp.open('POST', url);
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify(formdata));
    },
    createJob: function() {
        var requester = document.getElementById('inputRequester').value;
        var environment = document.getElementById('inputEnvironment').value;
        var test = document.getElementById('inputTest').value;

        var formdata = {'requester': requester, 'environment': environment,
                        'test': test};
        var resource = 'jobs/';
        var label = 'Job';
        this.sendFormData(formdata, resource, label);
    },
    createEnv: function() {
        var hostname = document.getElementById('inputHostname').value;
        var operating_system = document.getElementById('inputOperatingSystem').value;

        var formdata = {'hostname': hostname,
                        'operating_system': operating_system};
        var resource = 'environments/';
        var label = 'Environment';
        this.sendFormData(formdata, resource, label);
    },
    syncJobs: function() {
        if ( $.fn.dataTable.isDataTable( "#results") ) {
            var jobs_table = $( "#results" ).DataTable();
        } else {
            var jobs_table = $( "#results" ).dataTable({
                order: [[0, "desc"]],
                columns: [
                    { title: "Id", data: "id"},
                    { title: "Requester", data: "requester" },
                    { title: "Environment", data: "environment" },
                    { title: "Status", data: "status" },
                    { title: "Test", data: "test" },
                    { title: "Duration", data: "duration" },
                ],
                serverSide: true,
                ajax: function(data, callback, settings) {
                    options = {}
                    guacamoleServer.getJobs(options, function( json ) {
                            console.log(json.results)
                            $.each(json.results, function(index, value) {
                                /*value.tests_total = value.tests.length; */
                            });
                            callback({
                                recordsTotal: json.count,
                                recordsFiltered: json.count,
                                data: json.results,
                            });
                    });
                }
            });
        }

    },
    displayJobDetailsRefresh: function() {
        setInterval(this.displayJobDetails, 1000);
    },
    displayJobDetails: function() {
        var jobid = document.getElementById('inputJobID').value;
        var success = function(json) {
            $( "#job-id-2" ).text( json.id );
            $( "#job-requester" ).text( json.requester );
            $( "#job-environment" ).text( json.environment );
            $( "#job-test" ).text( json.test );
            $( "#job-status" ).text( json.status );
            $( "#job-duration" ).text( json.duration );
            $( "#job-output" ).text( json.output );
            $( "#job-details" ).show();
            $( "#job-output" ).show();
        };
        guacamoleServer.getJobById(jobid, success);
    },
    syncEnvironments: function() {
        if ( $.fn.dataTable.isDataTable( "#results-env") ) {
            var jobs_table = $("#results-env").DataTable();
        } else {
            var jobs_table = $( "#results-env" ).dataTable({
                order: [[0, "desc"]],
                columns: [
                    { title: "Id", data: "id"},
                    { title: "Hostname", data: "hostname" },
                    { title: "Operating System", data: "operating_system" },
                    { title: "Current Job", data: "current_job" },
                ],
                serverSide: true,
                ajax: function(data, callback, settings) {
                    options = {};
                    guacamoleServer.getEnvironments(options, function( json ) {
                            console.log(json.results)
                            $.each(json.results, function(index, value) {
                                /*value.tests_total = value.tests.length; */
                            });
                            callback({
                                recordsTotal: json.count,
                                recordsFiltered: json.count,
                                data: json.results,
                            });
                    });
                }
            });
        }

    }
};
