DROP TABLE IF EXISTS "organism";
CREATE TABLE "organism" (
    "id"   INTEGER NOT NULL PRIMARY KEY,
    "name" TEXT    NOT NULL
);

INSERT INTO organism (name) VALUES('Arabidopsis thaliana');
INSERT INTO organism (name) VALUES('Oryza sativa');
INSERT INTO organism (name) VALUES('Microtus californicus');
INSERT INTO organism (name) VALUES('Drosophila melanogaster');
INSERT INTO organism (name) VALUES('Danio rerio');
INSERT INTO organism (name) VALUES('Chlamydomonas reinhardtii');
INSERT INTO organism (name) VALUES('Solanum tuberosum');
