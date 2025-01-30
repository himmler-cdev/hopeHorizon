import { UserEntity } from "../../feature-user/entity/user.entity";

export interface UserSettingsDialog {
    user: UserEntity;
    deactivate: boolean;
}