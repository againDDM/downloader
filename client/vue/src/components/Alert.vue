<template>
  <div class="alert alert-primary" role="alert">
    {{ text }}
  </div>
</template>

<script>
export default {
  props: ['text'],
};
</script>
