/**
 * Copyright 2014 Solinea, Inc.
 *
 * Licensed under the Solinea Software License Agreement (goldstone),
 * Version 1.0 (the "License"); you may not use this file except in compliance
 * with the License. You may obtain a copy of the License at:
 *
 *     http://www.solinea.com/goldstone/LICENSE.pdf
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Author: Alex Jacobs
 */

var ServiceStatusView = Backbone.View.extend({

    defaults: {},

    initialize: function(options) {
        this.options = options || {};
        this.defaults = _.clone(this.defaults);
        this.defaults.url = this.collection.url;
        this.el = options.el;
        this.defaults.width = options.width;

        var ns = this.defaults;
        var self = this;

        // required in case spinner loading takes
        // longer than chart loading
        ns.spinnerDisplay = 'inline';

        var appendSpinnerLocation = ns.location;
        $('<img id="spinner" src="' + blueSpinnerGif + '">').load(function() {
            $(this).appendTo(appendSpinnerLocation).css({
                'position': 'relative',
                'margin-left': (ns.width / 2),
                'display': ns.spinnerDisplay
            });
        });

        this.collection.on('sync', function() {
            if (self.collection.defaults.setAchieved) {
                console.log('final set at sync: ', self.collection.length, self.collection.toJSON());

                self.update();

                self.collection.defaults.fetchInProgress = false;
                console.log('fetchInProgress?', self.collection.defaults.fetchInProgress);
                self.collection.defaults.setAchieved = false;
            }
        });
    },

    classSelector: function(item) {
        if (item === "running") {
            return 'alert alert-success';
        }
        return 'alert alert-danger fa fa-exclamation-circle';
    },

    collectionPrep: function() {
        var ns = this.defaults;
        var self = this;

        allthelogs = this.collection.toJSON();

        var data = allthelogs;
        console.log('just arriving in collectionPrep; len=', data.length);

        /*
        iterate through 'data, find the index at which point a duplicate appears, and truncate (slice) the array at that point.
        massage the array to be a simple object {name:true/false} and return it
        */

        var initialSetConstruction = {};

        for (var i = 0; i < data.length; i++) {

            var service = data[i].name;

            if (initialSetConstruction[service]) {
                console.log('dupe found at', i, data.length);
                data = data.slice(0, i);
                break;
            }

            initialSetConstruction[service] = true;
        }

        console.log('data.len before removing dupes = ', data.length);


        var finalData = [];


        /*
        figure out here how to push the object name as
        */
        _.each(data, function(item) {
            var resultObject = {};
            var resultName = item.name.slice(item.name.lastIndexOf('.') + 1);
            // console.log(resultName);
            resultObject[resultName] = item.value;
            finalData.push(resultObject);
        });
        console.log('final data.len after removing dupes = ', finalData.length);

        return finalData;

    },

    update: function() {

        var ns = this.defaults;
        var self = this;

        // sets css for spinner to hidden in case
        // spinner callback resolves
        // after chart data callback
        ns.spinnerDisplay = 'none';
        $(this.el).find('#spinner').hide();

        this.render();

        var allthelogs = this.collectionPrep();

        console.log('allthelogs from in update', allthelogs.length, allthelogs);

        // refreshes every 30 seconds
        setTimeout(function() {
            self.collection.retrieveData();
        }, 30000);

        // If we didn't receive any valid files, append "No Data Returned"
        if (allthelogs.length === 0) {

            // if 'no data returned' already exists on page, don't reapply it
            if ($(this.el).find('#noDataReturned').length) {
                return;
            }

            $('<span id="noDataReturned">No Data Returned</span>').appendTo(this.el)
                .css({
                    'position': 'relative',
                    'margin-left': $(this.el).width() / 2 - 14,
                    'top': -$(this.el).height() / 2
                });
            return;
        }

        // remove No Data Returned once data starts flowing again
        if ($(this.el).find('#noDataReturned').length) {
            $(this.el).find('#noDataReturned').remove();
        }

        var nodeNames = [];

        _.each(allthelogs, function(item) {
            nodeNames.push(item);
        });

        this.sorter(nodeNames);

        _.each(nodeNames, function(item, i) {

            var itemValue = _.values(nodeNames[i])[0];
            var itemKey = _.keys(nodeNames[i])[0];
            if (itemKey.length > 27) {
                itemKey = itemKey.slice(0, 27) + '...';
            }
            console.log(itemKey, itemValue);

            $(self.el).find('.mainContainer').append('<div style="width: 170px; height: 22px; font-size:11px; margin-bottom: 0; text-align:center; padding: 3px 0;" class="col-xs-1 toRemove ' + this.classSelector(itemValue) + '"> ' + itemKey + '</div>');
        }, this);
    },

    sorter: function(data) {

        return data.sort(function(a, b) {
            if (Object.keys(a) < Object.keys(b)) {
                return -1;
            }
            if (Object.keys(a) > Object.keys(b)) {
                return 1;
            } else {
                return 0;
            }
        });

    },

    render: function() {

        if ($(this.el).find('.mainContainer').length === 0) {
            this.$el.append(this.template());
            return this;
        } else {
            $(this.el).find('.mainContainer').empty();
        }

    },

    template: _.template("<div class='mainContainer'></div>")

});
