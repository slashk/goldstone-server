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

// define collection and link to model

var EventTimelineCollection = Backbone.Collection.extend({

    parse: function(data) {

        if(data.previous !== null){

            var dp = data.previous;
            var nextUrl = dp.slice(dp.indexOf('/core'));
            this.url = nextUrl;
            this.fetch({remove:false});
        }

        return data.results;
    },

    model: EventTimelineModel,

    initialize: function(options) {
        this.url = options.url;

        // adding {remove:false} to the initial fetch
        // will introduce an artifact that will
        // render via d3
        this.fetch();
    }
});
