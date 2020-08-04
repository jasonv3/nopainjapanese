<template>
  <div class="container">
    <ul class="list-group list-group-flush translated-box" v-for="(item, index) in translated" v-bind:key="index">
      <li class="list-group-item" >
        <p>
          <strong class="mr-2">{{ item[0]}}</strong>
          {{ item[1]}}
        </p>
      </li>
    </ul>
  </div>
</template>

<script>

export default {
  name: "Translation",
  components: {
  },
  data() {
    return {
      translated: []
    };
  },
  methods: {
    async getTransition(id) {
      const path = `/api/words/${id}`;
      const result = await this.$axios.get(path);
      return result.data
    }
  },
  async created() {
    const result = await this.getTransition(this.$route.params.id);
    this.translated = Object.entries(result);
    console.log(this.translated)
  }
};
</script>
