document.addEventListener('DOMContentLoaded', function () {
  // 搜索按钮：弹出输入框（可改为跳转 / 模糊搜索）
  const searchBtn = document.getElementById('searchBtn');
  searchBtn?.addEventListener('click', () => {
    const keyword = prompt('请输入搜索关键词：');
    if (keyword) {
      window.location.href = `/search?q=${encodeURIComponent(keyword)}`;
    }
  });

  // 打印按钮：调用浏览器打印
  const printBtn = document.getElementById('printBtn');
  printBtn?.addEventListener('click', () => {
    window.print();
  });

  // 添加笔记按钮：弹窗或跳转到笔记页面
  const noteBtn = document.getElementById('noteBtn');
  noteBtn?.addEventListener('click', () => {
    alert('📒 此处可集成个人笔记系统，如 Notion API 或本地存储功能');
  });

  // 阅读历史按钮：跳转历史页或显示弹窗
  const historyBtn = document.getElementById('historyBtn');
  historyBtn?.addEventListener('click', () => {
    alert('📜 历史功能尚未实现，可连接 LocalStorage 或用户记录系统');
  });

  // 通知中心按钮：示例提示
  const notifyBtn = document.getElementById('notifyBtn');
  notifyBtn?.addEventListener('click', () => {
    alert('🔔 当前暂无新通知，可与系统提醒模块联动');
  });

  // 用户按钮：示例弹窗
  const userBtn = document.getElementById('userBtn');
  userBtn?.addEventListener('click', () => {
    alert('👤 用户中心：支持登录 / 设置 / 同步数据（预留）');
  });
});