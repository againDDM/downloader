<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h3>Tasks</h3>
        <hr>
        <div class="input-group mb-3">
            <input type="text" class="form-control" placeholder="Input url" aria-label="Input url" aria-describedby="basic-addon2" v-model="target" >
            <div class="input-group-append">
                <span class="input-group-text btn btn-success btn-sm" id="basic-addon2" v-on:click="addTask">Download</span>
            </div>
        </div>
        <alert message="hi" variant="success"></alert>
        <div class="text-center" v-if="in_progress">
          <div class="spinner-border" role="status">
            <span class="sr-only">Загрузка...</span>
          </div>
        </div>
        <div class="text-center mt-1" v-else>
        </div>
        <h5>Your current tasks</h5>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Url</th>
              <th scope="col">Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(task, index) in tasks" :key="index">
              <td>{{ task.url }}</td>
              <td>{{ task.status }}</td>
              <td>
                <button type="button" class="btn btn-warning btn-sm" v-on:click="deleteTask(task.url)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import Alert from './Alert';

const path = 'http://localhost:5000/api/tasks/';
export default {
  data() {
    return {
      tasks: [],
      in_progress: false,
      target: ''
    };
  },
  methods: {
    addTask: async function () {
      this.in_progress = true;
      const response = await fetch(
          path, {
            method: 'POST',
            mode: 'cors',
            headers: {'Content-Type': 'application/json',},
            body: JSON.stringify({url: this.target}),
          }
        );
      const json = await response.json();
      this.target='';
      this.in_progress = false;
    },
    deleteTask: async function (target) {
      this.in_progress = true;
      const response = await fetch(
          path, {
            method: 'DELETE',
            mode: 'cors',
            headers: {'Content-Type': 'application/json',},
            body: JSON.stringify({url: target}),
          }
        );
      const json = await response.json();
      this.in_progress = false;
    },
    getTasks: async function () {
      const response = await fetch(path);
      const json = await response.json();
      this.tasks = json.tasks;
    },
  },
  components: {
    alert: Alert,
  },
  created() {
    this.getTasks();
  },
  updated() {
    this.getTasks();
  },
};
</script>
