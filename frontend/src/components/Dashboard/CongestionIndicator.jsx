import React from 'react';

export const CongestionIndicator = ({ level = 'LOW', size = 'md' }) => {
  const normalized = (level || 'LOW').toUpperCase();

  const config = {
    LOW: {
      bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
      dot: 'bg-emerald-400',
      label: 'Optimal (LOW)'
    },
    MEDIUM: {
      bg: 'bg-blue-500/10 border-blue-500/30 text-blue-400',
      dot: 'bg-blue-400',
      label: 'Moderate (MED)'
    },
    HIGH: {
      bg: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
      dot: 'bg-amber-400 animate-pulse',
      label: 'Heavy (HIGH)'
    },
    CRITICAL: {
      bg: 'bg-red-500/15 border-red-500/40 text-red-400 animate-pulse',
      dot: 'bg-red-500 animate-ping',
      label: 'Gridlock (CRIT)'
    }
  };

  const style = config[normalized] || config.LOW;
  const padding = size === 'sm' ? 'px-2 py-0.5 text-[10px]' : 'px-2.5 py-1 text-xs';

  return (
    <span className={`inline-flex items-center gap-1.5 font-bold rounded-md border ${style.bg} ${padding}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${style.dot}`} />
      {style.label}
    </span>
  );
};
