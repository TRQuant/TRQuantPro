/**
 * 性能监控工具
 */

interface PerformanceMetric {
  name: string;
  startTime: number;
  endTime?: number;
  duration?: number;
}

class PerformanceMonitor {
  private metrics: Map<string, PerformanceMetric> = new Map();

  /**
   * 开始计时
   */
  start(name: string): void {
    this.metrics.set(name, {
      name,
      startTime: performance.now(),
    });
  }

  /**
   * 结束计时
   */
  end(name: string): number | null {
    const metric = this.metrics.get(name);
    if (!metric) {
      console.warn(`[Performance] 未找到指标: ${name}`);
      return null;
    }

    const endTime = performance.now();
    const duration = endTime - metric.startTime;

    metric.endTime = endTime;
    metric.duration = duration;

    console.log(`[Performance] ${name}: ${duration.toFixed(2)}ms`);

    return duration;
  }

  /**
   * 获取指标
   */
  getMetric(name: string): PerformanceMetric | undefined {
    return this.metrics.get(name);
  }

  /**
   * 获取所有指标
   */
  getAllMetrics(): PerformanceMetric[] {
    return Array.from(this.metrics.values());
  }

  /**
   * 清除所有指标
   */
  clear(): void {
    this.metrics.clear();
  }

  /**
   * 报告性能指标
   */
  report(): void {
    const metrics = this.getAllMetrics();
    if (metrics.length === 0) {
      console.log('[Performance] 无性能指标');
      return;
    }

    console.group('[Performance Report]');
    metrics.forEach(metric => {
      if (metric.duration !== undefined) {
        console.log(`${metric.name}: ${metric.duration.toFixed(2)}ms`);
      }
    });
    console.groupEnd();
  }
}

// 单例
export const performanceMonitor = new PerformanceMonitor();

/**
 * 性能装饰器（用于函数）
 */
export function measurePerformance(name?: string) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    const metricName = name || `${target.constructor.name}.${propertyKey}`;

    descriptor.value = function (...args: any[]) {
      performanceMonitor.start(metricName);
      try {
        const result = originalMethod.apply(this, args);
        
        // 处理Promise
        if (result instanceof Promise) {
          return result.finally(() => {
            performanceMonitor.end(metricName);
          });
        }
        
        performanceMonitor.end(metricName);
        return result;
      } catch (error) {
        performanceMonitor.end(metricName);
        throw error;
      }
    };

    return descriptor;
  };
}

/**
 * React Hook: 测量组件渲染性能
 */
export function usePerformanceMeasure(componentName: string) {
  React.useEffect(() => {
    performanceMonitor.start(`${componentName}.render`);
    return () => {
      performanceMonitor.end(`${componentName}.render`);
    };
  });
}

// 需要导入React
import React from 'react';













































