import { HomeIcon, SearchIcon } from "lucide-react";
import Index from "./pages/Index.jsx";
import ObjectFinder from "./pages/ObjectFinder.jsx";

/**
 * Central place for defining the navigation items. Used for navigation components and routing.
 */
export const navItems = [
  {
    title: "Home",
    to: "/",
    icon: <HomeIcon className="h-4 w-4" />,
    page: <Index />,
  },
  {
    title: "Object Finder",
    to: "/object-finder",
    icon: <SearchIcon className="h-4 w-4" />,
    page: <ObjectFinder />,
  },
];
