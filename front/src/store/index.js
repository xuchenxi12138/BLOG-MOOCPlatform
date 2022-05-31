import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    logged: false,
    username: "",
    password: "",
    identification: "",
    avatarList: {
      "boy.svg": require("/src/assets/Avatars/boy.svg"),
      "cat.png": require("/src/assets/Avatars/cat.png"),
      "doctor.svg": require("/src/assets/Avatars/doctor.svg"),
      "dog.svg": require("/src/assets/Avatars/dog.svg"),
      "girl.svg": require("/src/assets/Avatars/girl.svg"),
      "github.svg": require("/src/assets/Avatars/github.svg"),
      "men.svg": require("/src/assets/Avatars/men.svg"),
      "women.svg": require("/src/assets/Avatars/women.svg"),
    },
    avatar: '',
    blogCreatorVisible:false,
    blogEditorVisible:false,
    routerList:[
      {
        path:"/",
        name:""
      }
    ],
    newAssignmentNumer:0,
    loginDialogVisible:false,
    
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
