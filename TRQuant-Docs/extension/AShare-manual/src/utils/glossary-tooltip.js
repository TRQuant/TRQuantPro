// 统一的金融术语悬浮提示工具
// 确保全局只显示一个提示框，避免重复显示

class GlossaryTooltip {
  constructor() {
    this.currentTooltip = null;
    this.hideTimeout = null;
    this.init();
  }

  init() {
    // 绑定事件监听器
    this.bindEvents();
    
    // 清理可能存在的旧提示框
    this.clearAllTooltips();
  }

  bindEvents() {
    // 监听鼠标进入事件
    document.addEventListener('mouseover', (event) => {
      if (event.target.classList.contains('glossary-term')) {
        this.showTooltip(event);
      }
    });

    // 监听鼠标离开事件
    document.addEventListener('mouseout', (event) => {
      if (event.target.classList.contains('glossary-term')) {
        this.hideTooltip();
      }
    });

    // 点击外部关闭提示框
    document.addEventListener('click', (event) => {
      if (!event.target.classList.contains('glossary-term') && 
          !event.target.closest('.tooltip')) {
        this.hideTooltip();
      }
    });

    // 窗口大小改变时重新定位
    window.addEventListener('resize', () => {
      this.repositionTooltip();
    });

    // 页面滚动时隐藏提示框
    window.addEventListener('scroll', () => {
      this.hideTooltip();
    });
  }

  showTooltip(event) {
    const term = event.target;
    const definition = term.getAttribute('data-definition');
    
    if (!definition) return;

    // 清除之前的隐藏定时器
    if (this.hideTimeout) {
      clearTimeout(this.hideTimeout);
      this.hideTimeout = null;
    }

    // 如果已有提示框，先移除
    this.hideTooltip();

    try {
      const data = JSON.parse(definition);
      
      // 创建工具提示
      const tooltip = document.createElement('div');
      tooltip.className = 'glossary-tooltip';
      tooltip.innerHTML = this.createTooltipHTML(data);

      // 定位工具提示
      this.positionTooltip(tooltip, term);

      // 添加到页面
      document.body.appendChild(tooltip);
      this.currentTooltip = tooltip;

      // 绑定提示框的鼠标事件
      tooltip.addEventListener('mouseenter', () => {
        if (this.hideTimeout) {
          clearTimeout(this.hideTimeout);
          this.hideTimeout = null;
        }
      });

      tooltip.addEventListener('mouseleave', () => {
        this.hideTooltip();
      });

    } catch (error) {
      console.warn('Failed to parse tooltip data:', error);
    }
  }

  hideTooltip() {
    // 清除之前的定时器
    if (this.hideTimeout) {
      clearTimeout(this.hideTimeout);
    }

    // 延迟隐藏，避免鼠标移动到提示框时立即消失
    this.hideTimeout = setTimeout(() => {
      if (this.currentTooltip) {
        this.currentTooltip.remove();
        this.currentTooltip = null;
      }
      this.hideTimeout = null;
    }, 100);
  }

  createTooltipHTML(data) {
    return `
      <div class="tooltip-header">${data.fullName || data.term}</div>
      <div class="tooltip-category">${data.category}</div>
      <div class="tooltip-description">${data.description}</div>
      ${data.example ? `<div class="tooltip-example">示例：${data.example}</div>` : ''}
      ${data.source ? `<div class="tooltip-source">来源：${data.source}</div>` : ''}
    `;
  }

  positionTooltip(tooltip, term) {
    const rect = term.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    // 初始位置
    let left = rect.left;
    let top = rect.bottom + 10;

    // 添加到页面以获取尺寸
    document.body.appendChild(tooltip);
    const tooltipRect = tooltip.getBoundingClientRect();

    // 检查右边界
    if (left + tooltipRect.width > viewportWidth) {
      left = viewportWidth - tooltipRect.width - 10;
    }

    // 检查下边界
    if (top + tooltipRect.height > viewportHeight) {
      top = rect.top - tooltipRect.height - 10;
    }

    // 确保不超出左边界
    if (left < 10) {
      left = 10;
    }

    // 确保不超出上边界
    if (top < 10) {
      top = rect.bottom + 10;
    }

    // 设置位置
    tooltip.style.left = left + 'px';
    tooltip.style.top = top + 'px';
  }

  repositionTooltip() {
    if (this.currentTooltip) {
      const activeTerm = document.querySelector('.glossary-term:hover');
      if (activeTerm) {
        this.positionTooltip(this.currentTooltip, activeTerm);
      }
    }
  }

  clearAllTooltips() {
    const existingTooltips = document.querySelectorAll('.glossary-tooltip, .tooltip');
    existingTooltips.forEach(tooltip => tooltip.remove());
    this.currentTooltip = null;
  }

  // 手动添加术语元素
  addGlossaryTerm(element, definition) {
    if (typeof definition === 'string') {
      element.setAttribute('data-definition', definition);
    } else {
      element.setAttribute('data-definition', JSON.stringify(definition));
    }
    element.classList.add('glossary-term');
  }

  // 批量添加术语
  addGlossaryTerms(terms) {
    terms.forEach(({ element, definition }) => {
      this.addGlossaryTerm(element, definition);
    });
  }

  // 销毁实例
  destroy() {
    this.clearAllTooltips();
    if (this.hideTimeout) {
      clearTimeout(this.hideTimeout);
    }
  }
}

// 全局实例
let globalGlossaryTooltip = null;

// 初始化函数
export function initGlossaryTooltip() {
  if (!globalGlossaryTooltip) {
    globalGlossaryTooltip = new GlossaryTooltip();
  }
  return globalGlossaryTooltip;
}

// 获取全局实例
export function getGlossaryTooltip() {
  return globalGlossaryTooltip;
}

// 销毁全局实例
export function destroyGlossaryTooltip() {
  if (globalGlossaryTooltip) {
    globalGlossaryTooltip.destroy();
    globalGlossaryTooltip = null;
  }
}

// 自动初始化
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    initGlossaryTooltip();
  });
}

// 导出类
export { GlossaryTooltip }; 
 