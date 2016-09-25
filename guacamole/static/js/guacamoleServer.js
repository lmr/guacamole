/*
 * Guacamole Server Javascript library.
 * Author: Lucas Meneghel Rodrigues <lookkas@gmail.com>
 */

var guacamoleServerSettings = {
    url: window.location.href,
};

var guacamoleServer = {
    init: function(settings) {
        guacamoleServer.settings = settings;
    },
    getVersion: function(success) {
        $.getJSON(this.settings.url + "version/", success);
    },
    getJobs: function(params, success) {
        console.log(params);
        $.getJSON(this.settings.url + "jobs/", params, success);
    },
    getEnvironments: function(params, success) {
        console.log(params);
        $.getJSON(this.settings.url + "environments/", params, success);
    },
    getLastJob: function(success) {
        $.getJSON(this.settings.url + "jobs/", {}, function ( json ) {
            success(json.results[0]);
        });
    },
    getJobById: function(id, success) {
        $.getJSON(this.settings.url + "jobs/" + id, {}, success);
    },
    getJobTrend: function(success) {
        $.getJSON(this.settings.url + "jobs/", {}, success);
    },
    getJobsSummary: function(success) {
        $.getJSON(this.settings.url + "jobs/summary/", success);
    },
    getTestsSummaryForJob: function(job_id, success) {
        $.ajax({
            url: this.settings.url + "jobs/" + job_id,
            type: "GET",
            async: false,
            dataType: 'json',
            success: success,
        });
    }
};
