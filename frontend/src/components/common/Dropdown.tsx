import { Menu, Transition } from '@headlessui/react';
import { Fragment, ReactNode } from 'react';
import { ChevronDownIcon } from '@heroicons/react/20/solid';
import clsx from 'clsx';

export interface DropdownItem {
  label: string;
  onClick: () => void;
  icon?: ReactNode;
  disabled?: boolean;
  danger?: boolean;
}

export interface DropdownProps {
  trigger: ReactNode;
  items: DropdownItem[];
  align?: 'left' | 'right';
}

export function Dropdown({ trigger, items, align = 'right' }: DropdownProps) {
  const alignStyles = {
    left: 'left-0 origin-top-left',
    right: 'right-0 origin-top-right',
  };

  return (
    <Menu as="div" className="relative inline-block text-left">
      <Menu.Button as="div" className="cursor-pointer">
        {trigger}
      </Menu.Button>

      <Transition
        as={Fragment}
        enter="transition ease-out duration-100"
        enterFrom="transform opacity-0 scale-95"
        enterTo="transform opacity-100 scale-100"
        leave="transition ease-in duration-75"
        leaveFrom="transform opacity-100 scale-100"
        leaveTo="transform opacity-0 scale-95"
      >
        <Menu.Items
          className={clsx(
            'absolute z-10 mt-2 w-56 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none',
            alignStyles[align]
          )}
        >
          <div className="py-1">
            {items.map((item, index) => (
              <Menu.Item key={index} disabled={item.disabled}>
                {({ active }) => (
                  <button
                    onClick={item.onClick}
                    className={clsx(
                      'group flex w-full items-center px-4 py-2 text-sm',
                      active && 'bg-gray-100',
                      item.disabled && 'opacity-50 cursor-not-allowed',
                      item.danger ? 'text-red-700' : 'text-gray-700'
                    )}
                  >
                    {item.icon && <span className="mr-3">{item.icon}</span>}
                    {item.label}
                  </button>
                )}
              </Menu.Item>
            ))}
          </div>
        </Menu.Items>
      </Transition>
    </Menu>
  );
}

export interface DropdownButtonProps {
  children: ReactNode;
  items: DropdownItem[];
  variant?: 'primary' | 'secondary';
}

export function DropdownButton({
  children,
  items,
  variant = 'secondary',
}: DropdownButtonProps) {
  const variantStyles = {
    primary: 'bg-primary-500 text-white hover:bg-primary-600',
    secondary: 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300',
  };

  return (
    <Dropdown
      trigger={
        <div
          className={clsx(
            'inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2',
            variantStyles[variant]
          )}
        >
          {children}
          <ChevronDownIcon className="ml-2 -mr-1 h-5 w-5" aria-hidden="true" />
        </div>
      }
      items={items}
    />
  );
}
