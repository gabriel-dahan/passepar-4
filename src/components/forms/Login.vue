<script setup lang="ts">
import Form from './Form.vue'
</script>

<template>
    <h1>P4</h1>
    <Form>
        <input type="text">
        <input type="text">
        <input type="text">
    </Form>
</template>


<style scoped>
h1 {

    color: red;


}

@media (min-width: 1024px) {
    header {
        display: flex;
        place-items: center;
        padding-right: calc(var(--section-gap) / 2);
    }

    .logo {
        margin: 0 2rem 0 0;
    }
}
</style>
