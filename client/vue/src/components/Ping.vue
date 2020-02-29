<template>
  <div class="container">
    <button type="button" class="btn btn-primary">{{ msg }}</button>
  </div>
</template>

<script>
export default {
  name: 'Ping',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    async getMessage() {
        const path = 'http://localhost:5000/ping';
        const response = await fetch(path);
        this.msg = await response.text();
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
