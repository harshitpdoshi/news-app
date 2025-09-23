export function formatRelativeTime(unixSeconds: number): string {
  if (!unixSeconds) {
    return 'just now';
  }

  const nowSeconds = Date.now() / 1000;
  const delta = Math.max(0, nowSeconds - unixSeconds);

  const intervals: { threshold: number; divisor: number; label: string }[] = [
    { threshold: 60, divisor: 1, label: 'second' },
    { threshold: 3600, divisor: 60, label: 'minute' },
    { threshold: 86400, divisor: 3600, label: 'hour' },
    { threshold: 604800, divisor: 86400, label: 'day' },
    { threshold: 2629743, divisor: 604800, label: 'week' },
    { threshold: 31556926, divisor: 2629743, label: 'month' }
  ];

  for (const { threshold, divisor, label } of intervals) {
    if (delta < threshold) {
      const value = Math.max(1, Math.floor(delta / divisor));
      return `${value} ${label}${value > 1 ? 's' : ''} ago`;
    }
  }

  const years = Math.max(1, Math.floor(delta / 31556926));
  return `${years} year${years > 1 ? 's' : ''} ago`;
}

export function extractHostname(url?: string): string | undefined {
  if (!url) {
    return undefined;
  }

  try {
    const hostname = new URL(url).hostname.replace(/^www\./, '');
    return hostname || undefined;
  } catch (error) {
    return undefined;
  }
}
