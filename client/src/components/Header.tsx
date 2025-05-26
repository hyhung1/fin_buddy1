import React, { useState } from "react";
import { BarChart3, UserCog, Moon } from "lucide-react";
import { Button } from "@/components/ui/button";
import useMobile from "@/hooks/use-mobile";
import { Link } from "wouter";

const Header: React.FC = () => {
  const isMobile = useMobile();
  const [isDarkMode, setIsDarkMode] = useState(true);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <header className="bg-white shadow-sm px-6 py-2 flex items-center justify-between border-b border-neutral-200">
      <div className="flex items-center">
        <Link href="/">
          <a className="flex items-center">
            <BarChart3 className="text-primary mr-2" />
            <h1 className="text-lg font-semibold text-neutral-800">Financial Analysis Buddy</h1>
          </a>
        </Link>
      </div>
      
      {!isMobile ? (
        <div className="flex items-center space-x-3">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium">Auto plot</span>
            <div 
              className={`w-10 h-5 flex items-center rounded-full p-1 cursor-pointer ${
                isDarkMode ? 'bg-green-500' : 'bg-gray-300'
              }`}
              onClick={toggleDarkMode}
            >
              <div 
                className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300 ${
                  isDarkMode ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </div>
          </div>
          <Button variant="outline" size="sm" className="bg-gray-50 hover:bg-gray-100 p-1.5">
            <Moon className="h-5 w-5" />
          </Button>
          <Button variant="outline" size="sm" className="bg-gray-50 hover:bg-gray-100 p-1.5">
            <UserCog className="h-5 w-5" />
          </Button>
        </div>
      ) : (
        <div className="flex items-center space-x-1.5">
          <div className="flex items-center gap-1.5">
            <span className="text-xs font-medium">Auto plot</span>
            <div 
              className={`w-8 h-4 flex items-center rounded-full p-0.5 cursor-pointer ${
                isDarkMode ? 'bg-green-500' : 'bg-gray-300'
              }`}
              onClick={toggleDarkMode}
            >
              <div 
                className={`bg-white w-3 h-3 rounded-full shadow-md transform transition-transform duration-300 ${
                  isDarkMode ? 'translate-x-4' : 'translate-x-0'
                }`}
              />
            </div>
          </div>
          <Button variant="outline" size="sm" className="bg-gray-50 hover:bg-gray-100 p-1">
            <Moon className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="sm" className="bg-gray-50 hover:bg-gray-100 p-1">
            <UserCog className="h-4 w-4" />
          </Button>
        </div>
      )}
    </header>
  );
};

export default Header;
