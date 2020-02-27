const url = '/api/tasks/'
var app = new Vue(
    {
        el: '#app',
        data: {
            latest:{
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
        methods: {
            getTasks: async function(){
                response = await fetch(url);
                const json = await response.json();
                this.latest.result = json.result;
                this.latest.status = response.status < 400 ? 'good': 'bad';
                this.latest.tasks = json.tasks;
            },
            addTask: async function(){
                this.current.status = 'unknow';
                this.current.result = 'validation...'
                response = await fetch(url, {method: 'POST',
                                             mode: 'cors',
                                             headers: {'Content-Type': 'application/json',},
                                             body: JSON.stringify({url: this.target}),
                                            }
                );
                const json = await response.json();
                this.current.result = json.result;
                this.current.status = response.status < 400 ? 'good': 'bad';
                this.current.tasks = json.tasks;
            },
            deleteTask: async function(){
                this.current.status = 'unknow';
                response = await fetch(url, {method: 'DELETE',
                                             mode: 'cors',
                                             headers: {'Content-Type': 'application/json',},
                                             body: JSON.stringify({url: this.target}),
                                            }
                );
                const json = await response.json();
                this.current.result = json.result;
                this.current.status = response.status < 400 ? 'good': 'bad';
                this.current.tasks = json.tasks;
            }
        }
    }
)
