/**
 * 懒加载组件Hook
 * 
 * 用于代码分割和性能优化
 */

import React, { Suspense, lazy, ComponentType } from 'react';
import LoadingIndicator from '../components/LoadingIndicator';

/**
 * 懒加载组件包装器
 */
export function useLazyComponent<T extends ComponentType<any>>(
  importFn: () => Promise<{ default: T }>,
  fallback?: React.ReactNode
) {
  const LazyComponent = React.useMemo(() => {
    return lazy(importFn);
  }, [importFn]);

  const WrappedComponent: React.FC<React.ComponentProps<T>> = (props) => {
    return (
      <Suspense fallback={fallback || <LoadingIndicator loading={true} />}>
        <LazyComponent {...props} />
      </Suspense>
    );
  };

  return WrappedComponent;
}

/**
 * 预定义的懒加载组件
 */
export const LazyWorkflowPage = lazy(() => import('../pages/Workflow'));
export const LazyTenbaggerPage = lazy(() => import('../pages/Tenbagger'));
export const LazyStrategyPage = lazy(() => import('../pages/Strategy'));

/**
 * 懒加载组件包装器（带默认加载状态）
 */
export function withLazyLoading<T extends ComponentType<any>>(
  Component: T,
  fallback?: React.ReactNode
) {
  return (props: React.ComponentProps<T>) => (
    <Suspense fallback={fallback || <LoadingIndicator loading={true} />}>
      <Component {...props} />
    </Suspense>
  );
}

