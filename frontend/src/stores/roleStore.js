import { defineStore } from 'pinia';
import { roleService } from '@/services/roleService';

export const useRoleStore = defineStore('role', {
  state: () => ({
    roles: [],
    currentRole: null,
    loading: false
  }),

  getters: {
    roleList: (state) => state.roles
  },

  actions: {
    async fetchRoles() {
      this.loading = true;
      try {
        const response = await roleService.getRoles();
        this.roles = response.data;
        return { success: true };
      } catch (error) {
        return {
          success: false,
          message: error.response?.data?.message || '获取角色列表失败'
        };
      } finally {
        this.loading = false;
      }
    },

    async fetchRoleById(id) {
      try {
        const response = await roleService.getRoleById(id);
        this.currentRole = response.data.role;
        return { success: true };
      } catch (error) {
        return {
          success: false,
          message: error.response?.data?.message || '获取角色信息失败'
        };
      }
    },

    async createRole(roleData) {
      try {
        const response = await roleService.createRole(roleData);
        this.roles.push(response.data.role);
        return { success: true, data: response.data };
      } catch (error) {
        return {
          success: false,
          message: error.response?.data?.message || '创建角色失败'
        };
      }
    },

    async updateRole(id, roleData) {
      try {
        const response = await roleService.updateRole(id, roleData);
        const index = this.roles.findIndex(role => role.id === id);
        if (index !== -1) {
          this.roles[index] = response.data.role;
        }
        return { success: true, data: response.data };
      } catch (error) {
        return {
          success: false,
          message: error.response?.data?.message || '更新角色失败'
        };
      }
    },

    async deleteRole(id) {
      try {
        await roleService.deleteRole(id);
        this.roles = this.roles.filter(role => role.id !== id);
        return { success: true };
      } catch (error) {
        return {
          success: false,
          message: error.response?.data?.message || '删除角色失败'
        };
      }
    }
  }
});