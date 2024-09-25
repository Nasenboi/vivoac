import { Address, AudioFormat } from "./general";

export interface UserConfig {
    audio_format?: AudioFormat;
}

export default interface User {
    id?: string;
    username?: string;
    first_name?: string;
    last_name?: string;
    email?: string;
    role?: "admin" | "user";
    address?: Address;
    phone_number_home?: string;
    phone_number_mobile?: string;
    disabled?: boolean;
    config?: UserConfig;
}

export interface UserForm extends User {
    password?: string;
}