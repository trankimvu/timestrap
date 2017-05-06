<clients>
    <p class="mb-4 clearfix">
        <pager update={ getClients }/>
    </p>

    <form class="row form-row mb-5 shadow-muted" onsubmit={ submitClient } if={ perms && perms.add_client }>
        <div class="col-10">
            <input type="text"
                   class="form-control form-control-lg"
                   ref="name"
                   placeholder="New Client Name"
                   required>
        </div>
        <div class="col-2">
            <button type="submit" class="btn btn-success btn-lg">
                Add
            </button>
        </div>
    </form>

    <client each={ clients } perms={ perms } />


    <script>
        getClients(url) {
            url = (typeof url !== 'undefined') ? url : clientsApiUrl;
            quickFetch(url).then(function(data) {
                this.update({
                    clients: data.results,
                    next: data.next,
                    previous: data.previous
                });
            }.bind(this));
        }


        submitClient(e) {
            e.preventDefault();
            let body = {
                name: this.refs.name.value
            };
            quickFetch(clientsApiUrl, 'post', body).then(function(data) {
                this.refs.name.value = '';
                if (data.id) {
                    this.clients.unshift(data);
                    this.update();
                }
            }.bind(this));
        }


        getPerms() {
            quickFetch('/api/permissions/').then(function(data) {
                   let perms = Object;
                   $.each(data.results, function(i, perm) {
                        perms[perm.codename] = perm;
                    });
                   this.perms = perms;
                });
        }

        this.on('mount', function() {
            this.getPerms();
            this.getClients();
        }.bind(this));
    </script>
</clients>
