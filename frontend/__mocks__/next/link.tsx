import React from "react";
// Simple Link mock — renders an anchor tag
const Link = ({ href, children, ...props }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
  <a href={href} {...props}>{children}</a>
);
export default Link;
