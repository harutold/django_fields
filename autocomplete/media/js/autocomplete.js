var Autocompleter = new Class({
    initialize: function(el) {
        this.el = $(el);
        if (! this.el ) throw 'Autocompleter shoud be initialized with a dom element';
        //var r = this.el.className.match(/__\w+__/);
        //if (r.length != 1) throw 'Bad url parameter for autocompleter';
        this.url = this.el.getNext().href
        this.el.getNext().remove()
        this.state = 'closed';
        this.list = new Element('div', {
            'class': 'autocompleter_list'
        }).injectInside(document.body);
        this.loading = new Element('div', {
            'class': 'autocompleter_loading'
        }).injectAfter(this.el);
        this.requested_value = '';
        this.createEvents();
    },
    onKeyup: function(ev) {
        if (! this.el.value) {
            this.closeList();
        }
        if (this.state == 'closed') {
            if (this.el.value) {
                this.makeRequest();
            }
            return true;
        } else if (this.state == 'opened') {
            if (ev.key == 'down' || ev.key == 'up') {
                this.moveCursor({'up': -1, 'down': 1}[ev.key]);
                return false;
            } else if (ev.key == 'esc') {
                this.closeList();
                return false;
            } else if (ev.key == 'enter' && this.position > -1) {
                this.el.value = this.list.getChildren()[this.position].$attributes.source_text;
                this.closeList();
                return true;
            }
            this.makeRequest();
            return true;
        }    
    },
    moveCursor: function(d) {
        this.list.getChildren().each(function(e){
            if (e.hasClass('selected')) {
                e.removeClass('selected');
            }
        });
        if (d<0 && this.position > 0)
            this.position += -1;
        else if (d>0 && this.position < this.list_length - 1)
            this.position += 1;
        this.list.getChildren()[this.position].addClass('selected');
    },
    makeRequest: function() {
        if (this.delay) {
            $clear(this.delay);
        }
        this.delay = function(){
            if (this.el.value && this.el.value != this.requested_value ) {
                this.requested_value = this.el.value;
                this.loading.setStyle('visibility', 'visible');
                new Request.JSON({
                    url: this.url,
                    onComplete: this.processResponse.bind(this)
                }).post({value: this.el.value});
            }
        }.bind(this).delay(500);
    },
    processResponse: function(r, t) {
        this.loading.setStyle('visibility', 'hidden');
        if (! r) {
            r = JSON.decode(t);
        }
        if ( r && r.success) {
            this.createList(r.items);
        }
    },
    createEvents: function() {
        this.el.addEvent('keyup', this.onKeyup.bind(this));
    },
    createList: function(items) {
        this.list.empty().setStyles({
            top: this.el.getTop() + this.el.getHeight(),
            left: this.el.getLeft(),
            width: this.el.getWidth()
        });
        items.each(function(item){
            var html, value;
            if (typeof item == 'string') {
                html = value = item;
            } else {
                value = item[0];
                html = item[1];
            }
            var i = new Element('div', {
                html: html,
                events: {
                    'mouseover': function() {
                        i.addClass('hover');
                    },
                    'mouseout': function() {
                        i.removeClass('hover');
                    },
                    'click': function() {
                        this.el.value = i.$attributes.source_text;
                        this.closeList();
                    }.bind(this)
                }
            }).injectInside(this.list);
            i.$attributes.source_text = value;
        }.bind(this));
        this.list_length = items.length;
        if (this.list_length) {
            this.list.setStyle('display', 'block');
            this.state = 'opened';
        } else {
            this.list.setStyle('display', 'none');
            this.state = 'closed';
        }
        this.position = -1;
    },
    closeList: function() {
        this.list.setStyle('display', 'none');
        this.state = 'closed';
    }
});

window.addEvent('domready', function(){
    $$('input.autocomplete').each(function(el){
        new Autocompleter(el);
    });
});