<template>
  <div class="container">
    <form id="addPostForm" v-if="sharedState.is_authenticated && sharedState.user_perms.includes('write')" @submit.prevent="onSubmit" class="g-mb-40">
      <div class="form-group" v-bind:class="{'u-has-error-v1': postForm.titleError}">
        <input type="text" v-model="postForm.title" class="form-control" id="postFormTitle" placeholder="标题">
        <small class="form-control-feedback" v-show="postForm.titleError">{{ postForm.titleError }}</small>
      </div>
      <div class="form-group">
        <textarea v-model="postForm.body" class="form-control" id="postFormBody" rows="5" placeholder=" 内容" maxlength="144"></textarea>
        <small>{{postForm.bodyLength}}/144</small>
        <small class="form-control-feedback" v-show="postForm.bodyError">{{ postForm.bodyError }}</small>
      </div>
      <div class="form-group">
        <textarea v-model="postForm.chinesebody" class="form-control" id="postFormBody" rows="5" placeholder=" 中文内容" maxlength="144"></textarea>
      </div>
      <div class="form-group">
        <div v-if="previewImage !== null" class="image-preview">
          <img v-bind:src="previewImage" class="uploading-image" style="max-width:320px;" />
          <button class="btn btn-danger btn-sm rounded-0" v-on:click="onDeleteImage" type="button" data-toggle="tooltip" data-placement="top" title="Delete"><i class="fa fa-trash"></i></button>
        </div>
        <input id="imageInput" type="file" accept="image/png, image/jpeg" v-on:change="onPreviewImage"/>
      </div>
      <div class="form-group">
        <div v-if="audioUrl !== null" class="audio-preview">
          <audio controls v-bind:src="audioUrl"></audio>
          <button class="btn btn-danger btn-sm rounded-0" v-on:click="onDeleteAudio" type="button" data-toggle="tooltip" data-placement="top" title="Delete"><i class="fa fa-trash"></i></button>
        </div>
        <!-- <button type="button" class="btn btn-primary" v-bind:class="{ active: isActive }" v-on:click="toggleRecordAudio">
          <i class="fa fa-microphone"></i>
        </button> -->
        <div class="record_btn" v-bind:class="{ active: isActive }" v-on:click="toggleRecordAudio">
          <i class="fa fa-microphone"></i>
        </div>
      </div>
      <div class="form-group">
        <vue-tags-input
          v-model="tag"
          :tags="tags"
          :autocomplete-items="filteredItems"
          @tags-changed="newTags => tags = newTags"
        />
        <!-- <input type="text" v-model="postForm.summary" class="form-control" id="postFormSummary" placeholder="摘要"> -->
      </div>
      <button type="submit" class="btn btn-primary">发布</button>
    </form>
  </div>
</template>

<script>
import store from '../store'
import axios from 'axios'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'
// 导入vue tag
import VueTagsInput from '@johmun/vue-tags-input';


export default {
  name: 'CreatePost',
  components: {
    VueTagsInput,
    VueMarkdown
  },
  data() {
    return {
      sharedState: store.state,
      tag: '',
      tags: [],
      autocompleteItems: [{
        text: '火影忍者',
      }, {
        text: '名侦探柯南',
      }, {
        text: '特朗普',
      }, {
        text: '富士山',
      }, {
        text: '京都',
      }],
      mediaRecorder: null,
      blob: null,
      audioUrl: null,
      isActive: false,
      message: null,
      previewImage: null,
      postForm: {
        title: '',
        summary: '',
        body: '',
        chinesebody: '',
        bodyLength: 0,
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null
      }
    }
  },
  watch: {
    postForm: {
      handler: function(newValue, oldValue) {
        this.postForm.bodyLength = newValue.body.length;
      },
      deep: true
    }
  },
  computed: {
    filteredItems() {
      return this.autocompleteItems.filter(i => {
        return i.text.toLowerCase().indexOf(this.tag.toLowerCase()) !== -1;
      });
    },
  },
  methods: {
    onDeleteImage() {
      this.previewImage = null;
      document.querySelector('#imageInput').value = null;
    },
    onDeleteAudio() {
      this.audioUrl = null;
    },
    async getMediaRecorder() {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          let mediaRecorder = null;
          await navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            mediaRecorder = new MediaRecorder(stream);
          });
          return mediaRecorder;
        } catch (error) {
          console.log('The following getUserMedia error occured: ' + err);
        }
      } else {
        console.log('getUserMedia not supported on your browser!');
      }
    },
    async toggleRecordAudio() {
      if (this.mediaRecorder === null) {
        await this.initMediaRecorder()
      }
      if (!this.isActive) {
        this.isActive = true;
        this.startRecording();
      } else {
        this.isActive = false;
        this.stopRecording();
      }
    },
    startRecording () {
      this.mediaRecorder.start();
      this.message = '录音中...';
    },
    stopRecording () {
      this.mediaRecorder.stop();
      this.message = '录音结束';
    },
    async onPreviewImage (e) {
      const image = e.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(image);
      const loadImage = () => {
        return new Promise((resolve, reject) => {
          reader.onload = e =>{
            this.previewImage = e.target.result;
            console.log('finish image load');
            resolve();
          };
          reader.onerror = e=> {
            reject();
          }
        });
      }
      await loadImage();
    },
    async getOssToken(token_type) {
      const path = `api/${token_type === 'audio' ? 'oss_audio_token' : 'oss_image_token'}`;
      try {
        const result = await this.$axios.get(path);
        return result.data;
      } catch (error) {
        console.error(error);
      }
    },
       async uploadAudio(oss_token) {
      let data = new FormData();
      const fileName = `${Date.now() + Math.random().toString(36).substring(7)}.ogg`;
      data.append('OSSAccessKeyId', oss_token.accessid);
      data.append('policy', oss_token.policy);
      data.append('Signature', '/+JXN3nI4H5RF9a/ko6A0iYZdQc=')
      data.append('key', oss_token.dir + fileName);
      data.append('file', this.blob);

      let config = {
        // url: path,
        baseURL: oss_token.host, 
        method: 'POST',
        data: data
      }
      const instance = axios.create(config)
      await instance();
      return `${oss_token.host}/${oss_token.dir}${fileName}`
    },
    async uploadImage(oss_token) {
      const file = document.querySelector('#imageInput').files[0];
      const extension = (() => {
        switch (file.type) {
          case 'image/jpeg':
            return 'jpg';
            break;
          case 'image/gif':
            return 'gif';
            break;
          case 'image/png':
            return 'png';
            break;
          default:
            return 'jpg';
            break;
        }
      })();
      const fileName = `${Date.now() + Math.random().toString(36).substring(7)}.${extension}`;
      let data = new FormData();
      data.append('OSSAccessKeyId', oss_token.accessid);
      data.append('policy', oss_token.policy);
      data.append('Signature','/+JXN3nI4H5RF9a/ko6A0iYZdQc=')
      data.append('key', oss_token.dir + fileName);
      data.append('file', file);

      let config = {
        // url: path,
        baseURL: oss_token.host, 
        method: 'POST',
        data: data
      }
      const instance = axios.create(config)
      await instance();
      return `${oss_token.host}/${oss_token.dir}${fileName}`
    },
    async addPost(imgossdir, oggossdir) {
      this.postForm.errors = 0  // 重置

      if (!this.postForm.title) {
        this.postForm.errors++
        this.postForm.titleError = 'Title is required.'
      } else {
        this.postForm.titleError = null
      }

      if (!this.postForm.body) {
        this.postForm.errors++
        this.postForm.bodyError = 'Body is required.'
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #postFormBody 上
        $('#addPostForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
      } else {
        this.postForm.bodyError = null
        $('#addPostForm .md-editor').closest('.form-group').removeClass('u-has-error-v1')
      }

      if (this.postForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/posts'
      const payload = {
        title: this.postForm.title,
        summary: this.postForm.summary,
        body: this.postForm.body,
        imgossdir,
        oggossdir,
        chinesebody: this.postForm.chinesebody
      }
      await this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.$toasted.success('Successed add a new post.', { icon: 'fingerprint' })
          this.$router.push('/')
        })
        .catch((error) => {
          // handle error
          for (var field in error.response.data.message) {
            if (field == 'title') {
              this.postForm.titleError = error.response.data.message[field]
            } else if (field == 'body') {
              this.postForm.bodyError = error.response.data.message[field]
            } else {
              this.$toasted.error(error.response.data.message[field], { icon: 'fingerprint' })
            }
          }
        });
    },
    async onSubmit (e) {
      let imgossdir = null, oggossdir = null;
      if (this.previewImage !== null) {
        const oss_image_token = await this.getOssToken('image');
        imgossdir = await this.uploadImage(oss_image_token);
      }
      if (this.audioUrl !== null) {
        const oss_audio_token = await this.getOssToken('audio');
        oggossdir = await this.uploadAudio(oss_audio_token);
      }
      await this.addPost(imgossdir, oggossdir);
    },
    async initMediaRecorder() {
      let chunks = [];
      this.mediaRecorder = await this.getMediaRecorder();
      this.mediaRecorder.ondataavailable = (e) => {
        chunks.push(e.data);
      }
      this.mediaRecorder.onstop = (e) => {
        this.blob = new Blob(chunks, { 'type': 'audio/ogg; codecs=opus' });
        chunks = [];
        this.audioUrl = window.URL.createObjectURL(this.blob);
        // uploadAudioToOss(blob);
        console.log('recorder stopped');
      }
    }
  }
}
</script>
