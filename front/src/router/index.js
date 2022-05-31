import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/Admin',
    name: 'Admin',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/admin/Admin.vue'),
    children: [
      {
        path: '/Admin',
        name: '/HomeManagement',
        component: () => import(/* webpackChunkName: "about" */ '../views/admin/HomeManagement.vue'),
      },
      {
        path: '/Admin/TeacherManagement',
        name: '/TeacherManagement',
        component: () => import(/* webpackChunkName: "about" */ '../views/admin/TeacherManagement.vue'),
      },
      {
        path: '/Admin/AdminManagement',
        name: '/AdminManagement',
        component: () => import(/* webpackChunkName: "about" */ '../views/admin/AdminManagement.vue'),
      },
      {
        path: '/Admin/StudentManagement',
        name: '/StudentManagement',
        component: () => import(/* webpackChunkName: "about" */ '../views/admin/StudentManagement.vue'),
      },
      {
        path: '/Admin/BlogManagement',
        name: '/BlogManagement',
        component: () => import(/* webpackChunkName: "about" */ '../views/admin/BlogManagement.vue'),
      },
      {
        path: '/Admin/ClassManagement',
        name: '/ClassManagement',
        component: () => import(/* webpackChunkName: "about" */ '../views/admin/ClassManagement.vue'),

      },
      {
        path: '/Admin/LessonManagement',
        name: '/LessonManagement',
        component: () => import(/* webpackChunkName: "about" */ '../views/admin/LessonManagement.vue'),
      },
    ]
  },
  {
    path: '/Teacher',
    name: 'teacher',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/teacher/Teacher.vue'),
    children: [
      {
        path: "/Teacher",
        name: "MyBlogs",
        component: () => import(/* webpackChunkName: "about" */ '../views/teacher/MyBlogs.vue'),
      },
      {
        path: "/Teacher/MyInfo",
        name: "MyInfo",
        component: () => import(/* webpackChunkName: "about" */ '../views/teacher/MyInfo.vue'),
      },
      {
        path: "/Teacher/ChangePassword",
        name: "ChangePassword",
        component: () => import(/* webpackChunkName: "about" */ '../views/teacher/ChangePassword.vue'),
      },
      {
        path: "/Teacher/ClassManagement",
        name: "ClassManagement",
        component: () => import(/* webpackChunkName: "about" */ '../views/teacher/ClassManagement.vue'),
        children: [
          {
            path: '/Teacher/ClassManagement',
            name: '/ClassList',
            component: () => import(/* webpackChunkName: "about" */ '../views/teacher/ClassList.vue'),
          },
          {
            path: '/Teacher/ClassManagement/StudentList',
            name: '/StudentList',
            component: () => import(/* webpackChunkName: "about" */ '../views/teacher/StudentList.vue'),
          },
          {
            path: '/Teacher/ClassManagement/Assignments',
            name: '/Assignments',
            component: () => import(/* webpackChunkName: "about" */ '../views/teacher/Assignments.vue'),
          }, {
            path: '/Teacher/ClassManagement/AssignmentDone',
            name: '/Assignments',
            component: () => import(/* webpackChunkName: "about" */ '../views/teacher/AssignmentDone.vue'),
          },
          {
            path: '/Teacher/ClassManagement/StudentList/StudentDetail',
            name: '/StudentDetail',
            component: () => import(/* webpackChunkName: "about" */ '../views/teacher/StudentDetail.vue'),
          }
        ]
      },
      {
        path: "/Teacher/LessonManagement",
        name: "LessonManagement",
        component: () => import(/* webpackChunkName: "about" */ '../views/teacher/LessonManagement.vue'),
        children: [
          {
            path: "/Teacher/LessonManagement",
            redirect: "/Teacher/LessonManagement/LessonList"
          },
          {
            path: "/Teacher/LessonManagement/LessonList",
            name: "LessonList",
            component: () => import(/* webpackChunkName: "about" */ '../views/teacher/LessonList.vue'),
          },
          {
            path: "/Teacher/LessonManagement/EditLesson",
            name: "EditLesson",
            component: () => import(/* webpackChunkName: "about" */ '../views/teacher/EditLesson.vue'),
          }
        ]
      }
    ]
  },
  {
    path: "/Student",
    name: "Student",
    component: () => import('/src/views/student/Student.vue'),
    children: [
      {
        path: "/Student",
        name: "ClassList",
        component: () => import('/src/views/student/ClassList.vue'),
      },
      {
        path: "/Student/MyInfo",
        name: "MyInfo",
        component: () => import('/src/views/student/MyInfo.vue'),
      },
      {
        path: "/Student/MyBlogs",
        name: "MyBlogs",
        component: () => import('/src/views/student/MyBlogs.vue'),
      },
      {
        path: "/Student/Assignment",
        name: "Assignment",
        component: () => import('/src/views/student/Assignment.vue'),
      }, 
      {
        path: "/student/ChangePassword",
        name: "ChangePassword",
        component: () => import(/* webpackChunkName: "about" */ '../views/student/ChangePassword.vue'),
      },
      {
        path: "/student/SearchClass",
        name: "SearchClass",
        component: () => import(/* webpackChunkName: "about" */ '../views/student/SearchClass.vue'),
      },
    ]
  },
  {
    path: '*',
    component: () => import('/src/views/NonePage'),
    name: 'error',
    meta: {
      title: '页面没找到'
    }
  },
  {
    path: '/NoConnection',
    component: () => import('/src/views/NoConnection'),
    name: 'NoConnection',
    meta: {
      title: '找不到服务器'
    }
  },
  {
    path: "/Lesson",
    name: "LessonView",
    component: () => import(/* webpackChunkName: "about" */ '../views/LessonView.vue'),
    children: [
    ]
  },
  {
    path: "/Search",
    name: "SearchView",
    component: () => import(/* webpackChunkName: "about" */ '../views/search/Search.vue'),
    children: [
      {
        path:"/Search",
        redirect:"/Search/Blog"
      },
      {
        path: "/Search/Blog",
        name: "BlogView",
        component: () => import(/* webpackChunkName: "about" */ '../views/search/Blog.vue'),
      },
      {
        path: "/Search/Lesson",
        name: "LessonView",
        component: () => import(/* webpackChunkName: "about" */ '../views/search/Lesson.vue'),
      },
    ]
  },
  {
    path:"/Blog",
    name:"Blog",
    component: () => import(/* webpackChunkName: "about" */ '../views/Blog.vue'),
  },

]

const router = new VueRouter({
  // mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
