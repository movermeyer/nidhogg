CREATE TABLE `minecraft_tokens` (
  `id`      BIGINT(20) UNSIGNED     NOT NULL,
  `access`  VARCHAR(36)
            CHARACTER SET utf8
            COLLATE utf8_general_ci NULL,
  `client`  VARCHAR(36)
            CHARACTER SET utf8
            COLLATE utf8_general_ci NULL,
  `created` TIMESTAMP               NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` BIGINT(255) UNSIGNED    NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `user_id` UNIQUE (`user_id`))
  CHARACTER SET = utf8
  COLLATE = utf8_general_ci
  ENGINE = INNODB;

CREATE INDEX `index_user_id` USING BTREE ON `minecraft_tokens` (`user_id`);

ALTER TABLE `minecraft_tokens`
ADD CONSTRAINT `lnk_minecraft_tokens_wp_users`
FOREIGN KEY (`id`)
REFERENCES `wp_users` (`ID`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;