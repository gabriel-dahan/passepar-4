<script setup lang="ts">
// ...
</script>

<template>
    <div class="form-container">
        <form @submit="$emit('submited')" onsubmit="return false;" novalidate>
            <slot></slot>
        </form>
    </div>
</template>

<style>
.form-container {
    display: flex;
    justify-content: center;
    /* 
    height: 100%;
    align-items: center; 
    */
}

.form-container > form {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 400px;
}

.form-container > form > h2 {
    color: var(--matrix-text);
    font-family: 'Share Tech Mono', cursive;
    text-align: center;
}

.form-container > form > .fields {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.form-container > form > .fields > .f-field {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.form-container > form > .fields > .f-field > label {
    text-transform: uppercase;
    font-family: 'Share Tech Mono', cursive;
}

.form-container > form > .fields > .f-field > input {
    outline: none;
    padding: 5px;
    border: 1px var(--matrix-text) solid;
    border-radius: 5px;
    font-family: 'Share Tech Mono', cursive;
    font-size: 14px;
    color: var(--color-text);
    background-color: rgb(31, 31, 31);
}

.form-container > form > .fields > .f-field > ::placeholder {
    font-family: 'Share Tech Mono', cursive;
    color: var(--color-small-text);
}

.form-container > form > .f-submit > input {
    width: 100%;
    border-color: var(--matrix-text);
    background-color: var(--matrix-text);
    padding: 5px;
    border-radius: 8px;
    border-style: solid;
    font-family: 'Share Tech Mono', cursive;
    transition-duration: 0.4s;
}

.form-container > form > .f-submit > input:hover {
    background-color: var(--color-background);
    border-color: var(--matrix-text);
    color: var(--matrix-text);
}

.form-container > form > .fields > .f-field > .f-error {
    color: var(--error-text);
    font-family: 'Share Tech Mono', cursive;
}
</style>