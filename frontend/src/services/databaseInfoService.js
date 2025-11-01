import apiClient from "../utils/request";

/**
 * 数据库信息服务相关 API
 */
export const databaseInfoService = {
  /**
   * 获取所有数据库列表
   */
  getDatabases(connectionId) {
    return apiClient.get(`/database-info/${connectionId}/databases`);
  },

  /**
   * 获取指定数据库的所有表（支持关键字模糊搜索）
   */
  getTables(connectionId, databaseName, keyword) {
    return apiClient.get(`/database-info/${connectionId}/databases/${databaseName}/tables`, {
      params: keyword ? { q: keyword } : {}
    });
  },

  /**
   * 获取数据表结构
   */
  getTableStructure(connectionId, databaseName, tableName) {
    return apiClient.get(`/database-info/${connectionId}/databases/${databaseName}/tables/${tableName}/structure`);
  },

  /**
   * 获取数据表数据（支持分页）
   */
  getTableData(connectionId, databaseName, tableName, { page = 1, per_page = 100 } = {}) {
    return apiClient.get(`/database-info/${connectionId}/databases/${databaseName}/tables/${tableName}/data`, {
      params: { page, per_page }
    });
  },

  /**
   * 执行自定义SQL查询
   */
  executeQuery(connectionId, { database_name, query }) {
    return apiClient.post(`/database-info/${connectionId}/execute`, {
      database_name,
      query
    });
  },

  /**
   * 关闭数据库连接
   */
  closeConnection(connectionId) {
    return apiClient.post(`/database-info/${connectionId}/close`);
  },

  /**
   * 导出选中的数据为SQL文件
   */
  exportDataToSql(connectionId, { database_name, table_name, selected_data, sql_types }) {
    return apiClient.post(
      `/database-info/${connectionId}/export-sql`,
      {
        database_name,
        table_name,
        selected_data,
        sql_types
      },
      {
        responseType: 'blob' // 重要：指定响应类型为blob以支持文件下载
      }
    );
  },

  /**
   * 导出多个数据库为SQL文件（包括表结构和数据）
   */
  exportDatabasesToSql(connectionId, { database_tables, database_names, sql_types }) {
    return apiClient.post(
      `/database-info/${connectionId}/export-databases-sql`,
      {
        database_tables,
        database_names, // 兼容旧格式
        sql_types
      },
      {
        responseType: 'blob' // 重要：指定响应类型为blob以支持文件下载
      }
    );
  },
};

export default databaseInfoService;

