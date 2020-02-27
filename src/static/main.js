const url = '/api/tasks/';
const app = new Vue(
    {
        el: '#app',
        data: {
            latest: {
                result: 'unknow',
                tasks: [],
                status: 'unknow'
            },
            current: {
                result: 'unknow',
                tasks: [],
                status: 'unknow'
            },
            target: ''
        },
        watch: {
            'current.result': function (val) {
                fetch(url).then(response => {
                    response.json().then(json => {
                        this.latest.result = json.result;
                        this.latest.status = response.status < 400 ? 'good' : 'bad';
                        this.latest.tasks = json.tasks;
                    });
                });
            }
        },
        methods: {
            addTask: async function () {
                this.current.status = 'unknow';
                this.current.result = 'validation...';
                const response = await fetch(url, {
                        method: 'POST',
                        mode: 'cors',
                        headers: {'Content-Type': 'application/json',},
                        body: JSON.stringify({url: this.target}),
                    }
                );
                const json = await response.json();
                this.current.result = json.result;
                this.current.status = response.status < 400 ? 'good' : 'bad';
                this.current.tasks = json.tasks;
            },
            deleteTask: async function () {
                this.current.status = 'unknow';
                const response = await fetch(url, {
                        method: 'DELETE',
                        mode: 'cors',
                        headers: {'Content-Type': 'application/json',},
                        body: JSON.stringify({url: this.target}),
                    }
                );
                const json = await response.json();
                this.current.result = json.result;
                this.current.status = response.status < 400 ? 'good' : 'bad';
                this.current.tasks = json.tasks;
            }
        }
    }
);