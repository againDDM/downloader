<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h3 class="text-center">Tasks</h3>
        <hr>
        <div class="input-group mb-3">
            <input type="text"
                   class="form-control"
                   placeholder="Input url"
                   aria-label="Input url"
                   aria-describedby="basic-addon2"
                   v-model="target">
            <div class="input-group-append">
                <span class="input-group-text btn btn-success btn-sm"
                      id="basic-addon2" v-on:click="addTask(target)">
                  Download
                </span>
            </div>
        </div>
        <div class="text-center" style="height: 20px;">
          <div class="spinner-border" role="status" v-if="in_progress">
            <span class="sr-only">in progress...</span>
          </div>
          <div class="alert"
               v-bind:class="[message.type]"
               role="alert"
               v-else-if="message.show">
            <button type="button" class="close" v-on:click="closeAlert()" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
            {{ message.text }}
          </div>
        </div>
        <hr>
        <h5 class="text-center">Your current tasks</h5>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Url</th>
              <th scope="col">Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-bind:class="[task.table_class]"
                v-for="(task, index) in tasks" :key="index">
              <td>{{ task.url }}</td>
              <td>{{ task.status }}</td>
              <td>
                <button type="button"
                        class="btn btn-warning btn-sm"
                        v-on:click="deleteTask(task.url)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
const path = 'http://192.168.10.2:5000/api/tasks/';
export default {
  data() {
    return {
      tasks: [],
      in_progress: false,
      message: {
        show: false,
        text: 'TEST',
        type: 'alert-secondary',
      },
      target: '',
    };
  },
  watch: {
    'message.text': async function () { // eslint-disable-line
      await this.getTasks();
    },
  },
  methods: {
    async addTask(target) {
      const TheTarget = (target || '').replace(/^\s+|\s+$/g, '');
      if ((typeof (target) === 'undefined') || !(TheTarget)) {
        await this.getTasks();
        return;
      }
      this.in_progress = true;
      try {
        const response = await fetch(
          path, {
            method: 'POST',
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: TheTarget }),
          },
        );
        const json = await response.json();
        this.message.text = `${json.result}: ${json.task}`;
        this.message.type = response.status === 200 ? 'alert-success' : 'alert-danger';
        this.target = '';
      } catch (err) {
        this.message.text = `${err.message}`;
        this.message.type = 'alert-danger';
      }
      this.message.show = true;
      this.in_progress = false;
    },
    async deleteTask(target) {
      this.in_progress = true;
      try {
        const response = await fetch(
          path, {
            method: 'DELETE',
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: target }),
          },
        );
        const json = await response.json();
        this.message.text = `${json.result}: ${json.task}`;
        this.message.type = response.status === 200 ? 'alert-warning' : 'alert-danger';
      } catch (err) {
        this.message.text = `${err.message}`;
        this.message.type = 'alert-danger';
      }
      this.message.show = true;
      this.in_progress = false;
    },
    async getTasks() {
      const response = await fetch(path);
      const json = await response.json();
      const tasks = [];
      for (const task of json.tasks) { // eslint-disable-line
        switch (task.status) {
          case 'WAIT':
            task.table_class = 'table-light';
            break;
          case 'SUCCESS':
            task.table_class = 'table-success';
            break;
          case 'FAILED':
            task.table_class = 'table-danger';
            break;
          case 'PROCESSED':
            task.table_class = 'table-primary';
            break;
          default:
            task.table_class = 'table-secondary';
            break;
        }
        tasks.push(task);
      }
      this.tasks = tasks;
    },
    closeAlert() {
      this.message.show = false;
      this.message.text = '';
      this.message.type = 'alert-secondary';
    },
  },
  created() {
    this.getTasks();
  },
};
</script>
