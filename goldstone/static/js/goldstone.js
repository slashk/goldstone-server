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
 * Author: John Stanford
 */

goldstone.namespace('goldstone.topology')
goldstone.namespace('goldstone.hostAvail')

goldstone.goldstone.topology.url = function (render) {
    "use strict";
    var url = "/topology"

    if (typeof render !== 'undefined') {
        url += "?render=" + render
    }
    return url
}

goldstone.goldstone.hostAvail.url = function () {
    "use strict";
    var url = "/logging/nodes"
    return url
}

