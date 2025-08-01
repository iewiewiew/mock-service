import { defineStore } from 'pinia';
import { userService } from '@/services/userService';

export const useUserStore = defineStore('user', {
  state: () => ({
    users: [],
    currentUser: null,
    pagination: {
      current_page: 1,
      total: 0,
      per_page: 10
    },
    loading: false
  }),

  getters: {
    userList: (state) => state.users,
    paginationInfo: (state) => state.pagination
  },

  actions: {
    async fetchUsers(params = {}) {
      this.loading = true;
      try {
        const response = await userService.getUsers(params);
        this.users = response.data;
        this.pagination = {
          current_page: response.data.current_page,
          total: response.data.total,
          per_page: response.data.per_page || 10
        };
        return { success: true };
      } catch (error) {
        return {
          success: false,
          message: error.response?.data?.message || '获取用户列表失败'
        };
      } finally {
        this.loading = false;
      }
    },

    async fetchUserById(id) {
      try {
        const response = await userService.getUserById(id);
        console.log('用户详情-------:', response.data)
        this.currentUser = response.data.user;
        return response.data;
      } catch (error) {
        return {
          success: false,
          message: error.response?.data?.message || '获取用户信息失败'
        };
      }
    },

    async createUser(userData) {
      try {
        const response = await userService.createUser(userData);
        this.users.unshift(response.data.user);
        return { success: true, data: response.data };
      } catch (error) {
        return {
          success: false,
          message: error.response?.data?.message || '创建用户失败'
        };
      }
    },

    async updateUser(id, userData) {
      try {
        const response = await userService.updateUser(id, userData);
        const index = this.users.findIndex(user => user.id === id);
        if (index !== -1) {
          this.users[index] = response.data.user;
        }
        return { success: true, data: response.data };
      } catch (error) {
        return {
          success: false,
          message: error.response?.data?.message || '更新用户失败'
        };
      }
    },

    async deleteUser(id) {
      try {
        await userService.deleteUser(id);
        this.users = this.users.filter(user => user.id !== id);
        return { success: true };
      } catch (error) {
        return {
          success: false,
          message: error.response?.data?.message || '删除用户失败'
        };
      }
    }
  }
});