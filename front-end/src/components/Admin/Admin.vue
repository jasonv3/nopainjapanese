<template>
  <div class="container g-pt-20">
    <div class="row">
      <!-- 左边菜单栏 -->
      <div class="col-lg-3 g-mb-50">
        <aside class="g-brd-around g-brd-gray-light-v4 rounded g-px-20 g-py-30">
          
          <h2 class="text-center g-color-primary g-font-weight-600 g-line-height-1 g-font-size-60 g-pos-rel g-mb-30">Admin</h2>
          
          <hr class="g-brd-gray-light-v4 g-my-30">
          
          <!-- 用户头像 -->
          <div v-if="user" class="text-center g-pos-rel g-mb-30">
            <div class="g-width-100 g-height-100 mx-auto mb-3">
              <img class="img-fluid rounded-circle g-brd-around g-brd-gray-light-v4 g-pa-2" v-bind:src="user._links.avatar" v-bind:alt="user.name || user.username">
            </div>

            <span class="d-block g-font-weight-500">{{ user.name || user.username }}</span>

            <router-link v-bind:to="{ path: `/user/${sharedState.user_id}` }">
              <span class="u-icon-v3 u-icon-size--xs g-color-white--hover g-bg-primary--hover rounded-circle g-pos-abs g-top-0 g-right-15 g-cursor-pointer" title="Go To Your Profile"
                    data-toggle="tooltip"
                    data-placement="top">
                <i class="icon-finance-067 u-line-icon-pro"></i>
              </span>
            </router-link>
          </div>
          <!-- End 用户头像 -->

          <hr class="g-brd-gray-light-v4 g-my-30">

          <!-- 菜单列表 -->
          <ul class="list-unstyled mb-0">
            <li class="g-pb-3">
              <router-link v-bind:to="{ name: 'AdminRoles' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" v-bind:class="isAdminRoles" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-media-127 u-line-icon-pro"></i></span>
                Roles
              </router-link>
            </li>
            <li class="g-pb-3">
              <router-link v-bind:to="{ name: 'AdminUsers' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" v-bind:class="isAdminUsers" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-finance-067 u-line-icon-pro"></i></span>
                Users
              </router-link>
            </li>
            <li class="g-pb-3">
              <router-link v-bind:to="{ name: 'AdminPosts' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-education-008 u-line-icon-pro"></i></span>
                Posts
              </router-link>
            </li>
            <li class="g-py-3">
              <router-link v-bind:to="{ name: 'AdminComments' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-finance-206 u-line-icon-pro"></i></span>
                Comments
              </router-link>
            </li>
          </ul>
          <!-- End 菜单列表 -->
        </aside>
      </div>
      <!-- End 左边菜单栏 -->

      <!-- 右边子路由匹配后，显示对应的组件 -->
      <div class="col-lg-9 g-mb-50">
        <div class="rounded g-brd-around g-brd-gray-light-v4 g-overflow-x-scroll g-overflow-x-visible--lg g-pa-30">
          <router-view></router-view>
        </div>
      </div>
      <!-- End 嵌套路由 -->
    </div>
  </div>
</template>

<script>
import store from '../../store'

export default {
  name: 'Admin',  // this is the name of the component
  data () {
    return {
      sharedState: store.state,
      user: ''
    }
  },
  computed: {
    isAdminRoles: function () {
      const tabs = ['AdminRoles', 'AdminUsers', 'AdminEditUser', 'AdminPosts', 'AdminComments']
      if (tabs.indexOf(this.$route.name) == -1) {
        return 'active g-color-primary--active g-bg-gray-light-v5--active'
      } else {
        return ''
      }
    },
    isAdminUsers: function () {
      if (this.$route.name == 'AdminEditUser') {
        return 'active g-color-primary--active g-bg-gray-light-v5--active'
      } else {
        return ''
      }
    }
  },
  methods: {
    getUser (id) {
      const path = `/api/users/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.user = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    }
  },
  created () {
    const user_id = this.sharedState.user_id
    this.getUser(user_id)
    // tooltip
    $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip(); 
    })
  }
}
</script>