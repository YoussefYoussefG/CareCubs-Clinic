import React from 'react';

type LogoSize = 'sm' | 'md' | 'lg' | 'xl';
type LogoVariant = 'color' | 'white' | 'dark';

interface LogoMarkProps {
  size?: LogoSize;
  variant?: LogoVariant;
  showText?: boolean;
  className?: string;
}

const sizeConfig = {
  sm: { icon: 32, text: 'text-sm', spacing: 'gap-2' },
  md: { icon: 48, text: 'text-lg', spacing: 'gap-3' },
  lg: { icon: 64, text: 'text-2xl', spacing: 'gap-4' },
  xl: { icon: 128, text: 'text-4xl', spacing: 'gap-6' },
};

const LogoMark: React.FC<LogoMarkProps> = ({
  size = 'md',
  variant = 'color',
  showText = true,
  className = '',
}) => {
  const { icon, text, spacing } = sizeConfig[size];

  const getTextColor = () => {
    switch (variant) {
      case 'white':
        return 'text-white';
      case 'dark':
        return 'text-slate-800';
      case 'color':
      default:
        return 'text-slate-800 dark:text-slate-200';
    }
  };

  const getSubTextColor = () => {
    switch (variant) {
      case 'white':
        return 'text-teal-200';
      case 'dark':
        return 'text-teal-700';
      case 'color':
      default:
        return 'text-teal-600 dark:text-teal-400';
    }
  };

  const getIconFills = () => {
    switch (variant) {
      case 'white':
        return {
          base: 'rgba(255, 255, 255, 0.9)',
          mid: 'rgba(255, 255, 255, 0.7)',
          light: 'rgba(255, 255, 255, 0.5)',
        };
      case 'dark':
        return {
          base: '#0F172A',
          mid: '#1E293B',
          light: '#334155',
        };
      case 'color':
      default:
        return {
          base: 'url(#logo-grad-1)',
          mid: 'url(#logo-grad-2)',
          light: 'url(#logo-grad-3)',
        };
    }
  };

  const fills = getIconFills();

  return (
    <div className={`flex flex-col items-center justify-center font-sans ${className}`}>
      <div className={`flex items-center justify-center ${showText ? '' : ''} animate-breathe`}>
        <svg
          width={icon}
          height={icon}
          viewBox="0 0 100 100"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {variant === 'color' && (
            <defs>
              <linearGradient id="logo-grad-1" x1="0" y1="0" x2="100" y2="100">
                <stop offset="0%" stopColor="#0D9488" />
                <stop offset="100%" stopColor="#10B981" />
              </linearGradient>
              <linearGradient id="logo-grad-2" x1="100" y1="0" x2="0" y2="100">
                <stop offset="0%" stopColor="#10B981" />
                <stop offset="100%" stopColor="#5EEAD4" />
              </linearGradient>
              <linearGradient id="logo-grad-3" x1="0" y1="50" x2="100" y2="50">
                <stop offset="0%" stopColor="#A7F3D0" />
                <stop offset="100%" stopColor="#10B981" />
              </linearGradient>
            </defs>
          )}
          
          {/* Left Ear */}
          <circle cx="25" cy="25" r="18" fill={fills.light} className="mix-blend-multiply opacity-80" />
          <circle cx="25" cy="25" r="12" fill={fills.mid} />
          
          {/* Right Ear */}
          <circle cx="75" cy="25" r="18" fill={fills.light} className="mix-blend-multiply opacity-80" />
          <circle cx="75" cy="25" r="12" fill={fills.mid} />
          
          {/* Main Face */}
          <circle cx="50" cy="55" r="40" fill={fills.base} className="mix-blend-multiply opacity-90" />
          
          {/* Inner Snout/Accent */}
          <circle cx="50" cy="65" r="25" fill={fills.mid} className="mix-blend-screen opacity-50" />
        </svg>
      </div>
      
      {showText && (
        <div className={`flex flex-col items-center mt-2 ${getTextColor()}`}>
          <span className={`${text} font-bold tracking-tight leading-none`}>
            CareCubs
          </span>
          <span className={`text-[0.65em] font-medium tracking-widest uppercase mt-1 ${getSubTextColor()}`}>
            Clinic
          </span>
        </div>
      )}
    </div>
  );
};

export default LogoMark;
