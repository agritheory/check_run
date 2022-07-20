<template>
  <div class="autocomplete" :class="{ 'isOpen': isOpen }">
    <input
      ref="mopInput"
      type="text"
      :id="`mop-input-${transactionIndex}`"
      @input="onChange"
      @focus="onChange"
      v-model="search"
      @keydown.down="onArrowDown"
      @keydown.up="onArrowUp"
      @keydown.enter="onEnter"
      class="form-control"
    />
    <ul
      id="autocomplete-results"
      v-show="isOpen"
      class="autocomplete-results"
    >
      <li
        class="loading"
        v-if="isLoading"
      >
        Loading results...
      </li>
      <li
        v-else
        v-for="(result, i) in results"
        :key="i"
        @click="setResult(result)"
        class="autocomplete-result"
        :class="{ 'is-active': i === arrowCounter }"
      >
        {{ result }}
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    name: 'ADropdown',
    props: {
      value: String,
      isOpen: Boolean,
      items: {
        type: Array,
        required: false,
        default: () => [],
      },
      isAsync: {
        type: Boolean,
        required: false,
        default: false,
      },
      transactionIndex: Number
    },
    data() {
      return {
        results: [],
        search: this.value,
        isLoading: false,
        arrowCounter: 0,
      };
    },
    watch: {
      items: function (value, oldValue) {
        if (value.length !== oldValue.length) {
          this.results = value;
          this.isLoading = false;
        }
      },
      value: function (value, oldValue) {
        if (value !== oldValue) {
          this.setResult(value)
        }
      }

    },
    mounted() {
      document.addEventListener('click', this.handleClickOutside)
      this.filterResults()
    },
    destroyed() {
      document.removeEventListener('click', this.handleClickOutside)
    },
    methods: {
      setResult(result) {
        this.search = result;
        this.closeResults()
      },
      filterResults() {
        this.results = this.items.filter((item) => {
          return item.toLowerCase().indexOf(this.search.toLowerCase()) > -1;
        });
      },
      onChange() {

        if (this.isAsync) {
          this.isLoading = true;
        } else {
          this.filterResults();

          this.isOpen = true
          this.$emit('isOpenChanged', this.isOpen)

        }
      },
      handleClickOutside(event) {
        if (!this.$el.contains(event.target)) {
          this.closeResults()
          this.arrowCounter = 0;
        }
      },
      closeResults() {

        this.isOpen = false
        this.$emit('isOpenChanged', this.isOpen)

        if(!this.items.includes(this.search)) {
          this.search = ''
        }
        if(this.value != this.search) {
          cur_frm.dirty();
        }
        this.value = this.search
        this.$emit('input', this.value)
      },
      onArrowDown() {
        if (this.arrowCounter < this.results.length) {
          this.arrowCounter = this.arrowCounter + 1;
        }
      },
      onArrowUp() {
        if (this.arrowCounter > 0) {
          this.arrowCounter = this.arrowCounter - 1;
        }
      },
      onEnter() {
        this.search = this.results[this.arrowCounter];
        this.closeResults()
        this.arrowCounter = 0;
      },
      openWithSearch() {
        this.search = ""
        this.onChange()
        this.$refs.mopInput.focus()
      }
    },
  };
</script>

<style>
  .autocomplete {
    position: relative;
  }

  .autocomplete-results {
    padding: 0;
    margin: 0;
    border: 1px solid #eeeeee;
    background-color: #f4f5f6;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
  }

  .autocomplete-result {
    list-style: none;
    text-align: left;
    padding: 4px 6px;
    cursor: pointer;

  }

  .autocomplete-result.is-active,
  .autocomplete-result:hover {
    background-color: #4590e8;
    color: white;
  }
</style>
