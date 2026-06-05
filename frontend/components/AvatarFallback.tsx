import React from "react";
import Image from "next/image";
import { FaUserCircle } from "react-icons/fa";

interface AvatarFallbackProps {
  src: string | null | undefined;
  alt: string;
  name?: string | null;
  className?: string;
  width?: number;
  height?: number;
  iconSize?: string;
}

export const AvatarFallback: React.FC<AvatarFallbackProps> = ({
  src,
  alt,
  name,
  className = "w-10 h-10 rounded-full object-cover",
  width = 1080,
  height = 1080,
  iconSize = "text-3xl"
}) => {
  const hasValidSrc = src && src !== "/default.jpg" && src !== "None" && src !== "null" && src !== "undefined";

  if (hasValidSrc) {
    return (
      <Image
        className={className}
        src={src}
        alt={alt}
        width={width}
        height={height}
      />
    );
  }

  // Get initials if name is provided
  const getInitials = (nameStr: string) => {
    if (!nameStr) return null;
    const parts = nameStr.split(" ").filter((p) => p.length > 0);
    if (parts.length === 0) return null;
    if (parts.length === 1) return parts[0].substring(0, 1).toUpperCase();
    return (parts[0].substring(0, 1) + parts[parts.length - 1].substring(0, 1)).toUpperCase();
  };

  const initials = name ? getInitials(name) : null;

  return (
    <div
      className={`${className.replace('object-cover', '')} flex items-center justify-center bg-gradient-to-br from-teal-400 to-emerald-500 text-white font-semibold`}
      title={name || alt}
    >
      {initials ? (
        <span>{initials}</span>
      ) : (
        <FaUserCircle className={iconSize} />
      )}
    </div>
  );
};

export default AvatarFallback;
