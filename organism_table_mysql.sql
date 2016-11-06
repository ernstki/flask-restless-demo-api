DROP TABLE `organism`
CREATE TABLE `organism` (
    `id`   INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO organism (name) VALUES('Arabidopsis thaliana');
INSERT INTO organism (name) VALUES('Oryza sativa');
INSERT INTO organism (name) VALUES('Microtus californicus');
INSERT INTO organism (name) VALUES('Drosophila melanogaster');
INSERT INTO organism (name) VALUES('Danio rerio');
INSERT INTO organism (name) VALUES('Chlamydomonas reinhardtii');
INSERT INTO organism (name) VALUES('Solanum tuberosum');
