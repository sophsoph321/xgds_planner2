//__BEGIN_LICENSE__
// Copyright (c) 2015, United States Government, as represented by the
// Administrator of the National Aeronautics and Space Administration.
// All rights reserved.
//
// The xGDS platform is licensed under the Apache License, Version 2.0
// (the "License"); you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0.
//
// Unless required by applicable law or agreed to in writing, software distributed
// under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the License.
//__END_LICENSE__

app.views = app.views || {};

app.views.PlanLinksView = Backbone.View.extend({
    template: '#template-plan-links',
    initialize: function() {
        var source = $(this.template).html();
        if (_.isUndefined(source)) {
            this.template = function() {
                return '';
            };
        } else {
            this.template = Handlebars.compile(source);
        }
    },
    render: function() {
        this.$el.html(this.template({
            planLinks: app.planLinks,
            planUuid: app.currentPlan.get('uuid'),
            planId: app.currentPlan.get('serverId')
        }));
        var callback = app.options.XGDS_PLANNER2_LINKS_LOADED_CALLBACK;
        if (callback != null) {
            callback(this.$el);
        }
    }
});