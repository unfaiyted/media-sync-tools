
export type MenuItem = {
    label: string;
    action?: () => void;
    icon?: any; // This would ideally be a Vue component type.
    subMenu?: MenuItem[];
}


export interface DividerItem {
    class?: '';
    type: 'divider';

}

export type MenuRow = MenuItem | MenuItem[] | DividerItem
