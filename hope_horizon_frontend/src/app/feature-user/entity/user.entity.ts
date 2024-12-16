import { UserDto } from "../dto/user.dto";

export class UserEntity {
    id? : number;
    username?: string;
    password?: string;
    email?: string;
    birthdate?: Date;
    user_role_id?: number;

    toDto(): UserDto {
        return {
            id: this.id,
            username: this.username,
            password: this.password,
            email: this.email,
            birthdate: this.birthdate?.toISOString(),
            user_role_id: this.user_role_id
        };
    }

    static fromDto(dto: UserDto): UserEntity {
        const entity = new UserEntity();
        entity.id = dto.id;
        entity.username = dto.username;
        entity.password = dto.password;
        entity.email = dto.email;
        entity.birthdate = dto.birthdate ? new Date(dto.birthdate) : undefined;
        entity.user_role_id = dto.user_role_id;
        return entity;
    }
}